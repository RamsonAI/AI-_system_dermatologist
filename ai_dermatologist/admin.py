from django.contrib import admin
from . models import Patients, Profile,DiagnosisReport

# Register your models here.

admin.site.register(Patients)
admin.site.register(Profile)
admin.site.register(DiagnosisReport)