from django.db import models

from role.models import *

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100, null=True)
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} v{self.version}"
    
class DynamicField(models.Model):
    model_name = models.CharField(max_length=100)
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=50)
    default = models.CharField(max_length=100, blank=True, null=True)
    max_length = models.IntegerField(blank=True, null=True)
    nullable = models.BooleanField(default=True)
    blank = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'dynamic_field'