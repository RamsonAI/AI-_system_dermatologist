from django.contrib import admin
from . models import Patients, Profile

# Register your models here.

admin.site.register(Patients)
admin.site.register(Profile)