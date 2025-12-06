from django.urls import path
from .views import (
    StudentListView, StudentCreateView, StudentUpdateView, 
    StudentDeleteView, DashboardView, StudentDetailView, export_students_csv,
    remove_student_photo
)

urlpatterns = [
    # Dashboard is the main page
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Student List & Management
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/add/', StudentCreateView.as_view(), name='student_add'),
    
    # Export CSV Link
    path('students/export/', export_students_csv, name='student_export'),
    
    # Detail, Edit, Delete (using slug)
    path('students/<slug:slug>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<slug:slug>/edit/', StudentUpdateView.as_view(), name='student_edit'),
    path('students/<slug:slug>/delete/', StudentDeleteView.as_view(), name='student_delete'),
    path('students/<slug:slug>/remove-photo/', remove_student_photo, name='student_remove_photo'),
]