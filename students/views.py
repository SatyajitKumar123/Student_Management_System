import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from .models import Student
from .forms import StudentForm

# --- DASHBOARD VIEW ---
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Total Students
        context['total_students'] = Student.objects.count()
        
        # 2. Students per Course (for Pie Chart)
        course_data = Student.objects.values('course').annotate(count=Count('id'))
        context['course_labels'] = [item['course'] for item in course_data]
        context['course_counts'] = [item['count'] for item in course_data]
        
        # 3. Enrollment over Time (for Line Chart) - Group by Month
        enrollment_data = Student.objects.annotate(
            month=TruncMonth('enrollment_date')
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        context['enrollment_labels'] = [item['month'].strftime('%b %Y') for item in enrollment_data]
        context['enrollment_counts'] = [item['count'] for item in enrollment_data]
        
        return context

# --- LIST VIEW WITH FILTERS ---
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Student.objects.all().order_by('-enrollment_date')
        
        # Text Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(enrollment_number__icontains=query)
            )
            
        # Course Filter
        course_filter = self.request.GET.get('course')
        if course_filter:
            queryset = queryset.filter(course=course_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass course choices to template for the dropdown
        context['course_choices'] = Student.CourseChoices.choices
        # Pass current filter to keep dropdown selected
        context['current_course'] = self.request.GET.get('course', '')
        # Pass current search query
        context['current_query'] = self.request.GET.get('q', '')
        return context
    
    def get_template_names(self):
        if self.request.htmx:
            return ['students/partials/student_list_results.html']
        return ['students/student_list.html']

# --- DETAIL VIEW (PROFILE) ---
class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

# --- EXPORT FUNCTION ---
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email', 'Enrollment No', 'Course', 'DOB'])

    queryset = Student.objects.all().order_by('last_name')
    
    # Apply Course Filter if present in URL
    course_filter = request.GET.get('course')
    if course_filter:
        queryset = queryset.filter(course=course_filter)

    for student in queryset:
        writer.writerow([
            student.first_name, 
            student.last_name, 
            student.email, 
            student.enrollment_number, 
            student.get_course_display(),
            student.date_of_birth
        ])

    return response

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
    extra_context = {'title': 'Add New Student'}

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student_list')
    extra_context = {'title': 'Edit Student'}
    # Note: UpdateView automatically looks for 'slug' in URL if 'pk' is missing

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    
# --- NEW: INSTANT PHOTO REMOVE ---
@require_POST
def remove_student_photo(request, slug):
    student = get_object_or_404(Student, slug=slug)
    
    # 1. Delete the file from filesystem and database field immediately
    if student.photo:
        student.photo.delete(save=True)
        
    # 2. Return the "Empty State" HTML (just the file input)
    # This allows the user to immediately upload a new one if they want
    context = {'form': StudentForm()} 
    return render(request, 'students/partials/photo_field.html', context)