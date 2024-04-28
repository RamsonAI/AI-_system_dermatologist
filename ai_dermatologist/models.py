from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Patients(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=6)
    registered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Patients'

    def __str__(self):
        return self.fullname


