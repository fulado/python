from django.db import models

# Create your models here.

class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
