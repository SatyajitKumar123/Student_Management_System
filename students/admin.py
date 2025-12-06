from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('first_name', 'last_name', 'enrollment_number', 'course', 'enrollment_date')
    
    # Fields to search via the search bar
    search_fields = ('first_name', 'last_name', 'enrollment_number', 'email')
    
    # Sidebar filters
    list_filter = ('course', 'enrollment_date')
    
    # Organize the detail view field layout
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth')
        }),
        ('Academic Details', {
            'fields': ('enrollment_number', 'course', 'slug')
        }),
    )
    
    # Make slug read-only since it is auto-generated in models.py
    readonly_fields = ('slug', 'enrollment_date')