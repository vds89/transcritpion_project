from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='processed/', null=True, default=None)

class CustomUser(AbstractUser):
    # Add any additional fields you need for your user model
    email = models.EmailField(unique=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',  # Change this to your preferred name
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',  # Change this to your preferred name
        help_text='Specific permissions for this user.',
    )
