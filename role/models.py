from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=120)
    module_name = models.CharField(max_length=120)
    access = models.CharField(max_length=120)
    class Meta:
        db_table = "role"
    def __str__(self):
        return f"{self.name} - {self.module_name}"

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='details')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_details"

    def __str__(self):
        return f"{self.user.username} - {self.role}"