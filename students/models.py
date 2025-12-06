import os
import uuid
from PIL import Image  # <--- NEW IMPORT
from django.db import models
from django.utils.text import slugify

# --- Rename Function ---
def student_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
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
    
    # Photo field
    photo = models.ImageField(upload_to=student_file_path, blank=True, null=True)
    
    bio = models.TextField(blank=True, help_text="Short student biography")
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    course = models.CharField(
        max_length=3, 
        choices=CourseChoices.choices, 
        default=CourseChoices.COMPUTER_SCIENCE
    )
    
    def save(self, *args, **kwargs):
        # 1. Generate Slug if missing
        if not self.slug:
            base_slug = f"{self.first_name} {self.last_name} {self.enrollment_number}"
            self.slug = slugify(base_slug)
            
        # 2. Save the data first (so the file exists on disk)
        super().save(*args, **kwargs)

        # 3. Image Compression Logic
        if self.photo:
            try:
                img_path = self.photo.path
                img = Image.open(img_path)
                
                # Check if image needs resizing (if larger than 800x800)
                if img.height > 800 or img.width > 800:
                    output_size = (800, 800)
                    img.thumbnail(output_size)
                    
                    # Save it back to the same path with optimization
                    # optimize=True and quality=70 reduces size drastically (e.g., 5MB -> 100KB)
                    img.save(img_path, optimize=True, quality=70)
            except Exception as e:
                # If something goes wrong (e.g., file permission), just pass
                pass

    def __str__(self):
        return f"{self.first_name} {self.last_name}"