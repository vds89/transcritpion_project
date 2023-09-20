from django.db import models

# Create your models here.
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    processed_file = models.FileField(upload_to='processed/', null=True, default=None)
