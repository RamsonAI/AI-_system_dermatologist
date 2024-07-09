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
    # dob = models.DateField(blank=True)
    gender = models.CharField(max_length=6)
    registered_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f"{self.fullname} - {self.email} - {self.gender}"

class DiagnosisReport(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    result = models.CharField(max_length=60)
    image = models.ImageField(upload_to='diagnosis_images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.fullname} - {self.result} - {self.created_at}"
