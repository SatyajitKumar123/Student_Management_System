import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Student

# 1. Delete file when Student object is deleted
@receiver(post_delete, sender=Student)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Student` object is deleted.
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

# 2. Delete old file when Photo is updated or cleared
@receiver(pre_save, sender=Student)
def delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem when corresponding `Student` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Student.objects.get(pk=instance.pk).photo
    except Student.DoesNotExist:
        return False

    new_file = instance.photo

    # If there was an old file, and it's different from the new one (or new one is None)
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)