from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.conf import settings
import uuid
from django.utils import timezone

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='processed/', null=True, default=None)

class EmailConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_confirmed = models.BooleanField(default=False)

class CustomUser(AbstractUser):
    # Add any additional fields you need for your user model
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=255, null=True, blank=True)

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
