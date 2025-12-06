import os
import uuid
from django.db import models
from django.utils.text import slugify

# --- 1. Define the renaming function ---
def student_file_path(instance, filename):
    """
    Generate file path: student_photos/UUID.jpg
    This prevents filename conflicts and hides the original filename.
    """
    ext = filename.split('.')[-1] # Get the file extension (e.g., jpg)
    filename = f'{uuid.uuid4()}.{ext}' # Generate a random UUID
    # Result: student_photos/550e8400-e29b-41d4-a716-446655440000.jpg
    return os.path.join('student_photos/', filename)

class Student(models.Model):
    class CourseChoices(models.TextChoices):
        COMPUTER_SCIENCE = 'CS', 'Computer Science'
        ENGINEERING = 'ENG', 'Engineering'
        BUSINESS = 'BUS', 'Business'
        ARTS = 'ART', 'Arts'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)
    
    # --- 2. Update the photo field to use the function ---
    # We removed 'student_photos/' string and passed the function instead
    photo = models.ImageField(upload_to=student_file_path, blank=True, null=True)
    
    bio = models.TextField(blank=True, help_text="Short student biography")
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    course = models.CharField(
        max_length=3, 
        choices=CourseChoices.choices, 
        default=CourseChoices.COMPUTER_SCIENCE
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = f"{self.first_name} {self.last_name} {self.enrollment_number}"
            self.slug = slugify(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"