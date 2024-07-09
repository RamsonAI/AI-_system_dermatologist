from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Patients, Profile, DiagnosisReport
from django.core.files.storage import FileSystemStorage
from .model import model, transform
from PIL import Image
import torch

# Create your views here.
@never_cache
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password.")
            return redirect('index')
    return render(request, 'login.html')

@never_cache
def index(request):
    return render(request, 'dermatologist/login.html')

@never_cache
def changePassword(request):
    return render(request, 'dermatologist/changePassword.html')

@never_cache
def changepassword2(request):
    return render(request, 'dermatologist/changepassword2.html')

@never_cache
def passwordchangedsuccess(request):
    return render(request, 'dermatologist/passwordchangedsucess.html')

@never_cache
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user is not None:
            return render(request, 'dermatologist/changepassword2.html', {'username': username})
        else:
            return render(request, 'dermatologist/changePassword.html', {'error': 'Username not found.'})
    return render(request, 'dermatologist/changePassword.html')

@never_cache
def Update_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('passwordchangedsuccess')
        else:
            return render(request, 'dermatologist/changePassword.html', {'error': 'username not found'})
    return redirect('changePassword')

# register patients view
@login_required(login_url='/')
@never_cache
def register(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        if fullname and email and gender and age:
            patient = Patients.objects.create(
                fullname=fullname,
                email = email,
                gender = gender,
                age=age
            )
            messages.success(request, 'Patient registered successfully')
            return redirect('patientslist')
        else:
            messages.error(request, 'Invalid inputs')
    else:
        render(request, 'patients.html')

@login_required(login_url='/')
@never_cache
def update_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        #retrieve the current user 
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        messages.success(request, 'your profile has been updated successfully!')
        return redirect('userprofile')
    else:
        return render(request, 'dermatologist/userprofile.html')

@login_required(login_url='/')
@never_cache
def patients_list(request):
    patients = Patients.objects.order_by('-registered_date')
    return render(request, 'dermatologist/patients.html', {'patients':patients})

@login_required(login_url='/')
@never_cache
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='/') 
@never_cache
def dashboard(request):
    total_patients = Patients.objects.count()
    total_reports =  DiagnosisReport.objects.count()

    context = {
        'total_patients' : total_patients,
        'total_reports' : total_reports
    }
    return render(request, 'dermatologist/dashboard.html', context)

# @login_required
# def count_reports(request):
#     total_reports = DiagnosisReport.objects.count()
#     return render(request, 'dermatologist/dashboard.html', {'total_reports':total_reports})

@login_required(login_url='/')
@never_cache
def userprofile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'dermatologist/userprofile.html', {'profile':profile})

@login_required(login_url='/')
@never_cache
def patients(request):
    return render(request, 'dermatologist/patients.html')

@login_required
def registerPatients(request):
    pass

@login_required(login_url='/')
@never_cache
def diagnosis(request):
    diagnosis_patients = Patients.objects.order_by('-registered_date')
    return render(request, 'dermatologist/diagnosis.html', {'diagnosis_patients':diagnosis_patients})

@login_required(login_url='/')
@never_cache
def patientsreport(request):
    reports = DiagnosisReport.objects.order_by('-created_at')
    return render(request, 'dermatologist/patientsreport.html', {'reports':reports})

# @login_required
# def graph_analysis(request):
#     male_count = Patients.objects.filter(gender='male').count()
#     female_count = Patients.objects.filter(gender='female').count()

#     context = {
#         'male_count':male_count,
#         'female_count':female_count,
#     }

#     return render(request, 'dermatologist/Analytics.html', context)

@login_required(login_url='/')
@never_cache
def Analytics(request):
    male_count = Patients.objects.filter(gender='male').count()
    female_count = Patients.objects.filter(gender='female').count()

    context = {
        'male_count':male_count,
        'female_count':female_count,
    }
    return render(request, 'dermatologist/Analytics.html', {'context':context})

@login_required(login_url='/')
@never_cache
def patientreport(request):
    return render(request, 'dermatologist/patientreport.html')

@login_required(login_url='/')
@never_cache
def newPatientRegistration(request):
    return render(request, 'dermatologist/newpatientregister.html')

@login_required(login_url='/')
@never_cache
def result(request):
    return render(request, 'dermatologist/result.html')

# def classify_image(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         image = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image.name, image)
#         file_url = fs.url(filename)

#         img = Image.open(image)
#         img = transform(img).unsqueeze(0)

#         with torch.no_grad():
#             outputs = model(img)
#             _, predicted = torch.max(outputs, 1)
#             #add logic for decoding the predicted class, e.g., 0 1
#             if predicted.item() == 0:
#                 result = "Acne"
#             elif predicted.item() == 1:
#                 result = "Scabies"
#             else:
#                 result = "Image is not recognized as acne or scabies"
            
#         return render(request, 'dermatologist/result.html', {'result': result, 'file_url':file_url })
#     return render(request, 'dermatologist/upload.html')


@login_required(login_url='/')
@never_cache
def classify_image(request):
    if request.method == 'POST' and request.FILES['image-choosed']:
        image = request.FILES['image-choosed']
        patient_id = request.POST['patient_id']
        patient = Patients.objects.get(id=patient_id)

        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)

        img = Image.open(image)
        img = transform(img).unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            outputs = model(img)
            _, predicted = torch.max(outputs, 1)
            if predicted.item() == 0:
                result = "Scabies have not been detected in the patient's image uploaded"
            elif predicted.item() == 1:
                result = "Scabies have been detected in the patient's image uploaded"
            else:
                result = 'Image unrecognized'

        #save the diagnosis report to the database
        diagnosis_report = DiagnosisReport(patient=patient, result=result, image=filename)
        diagnosis_report.save()

        return render(request, 'dermatologist/diagnosis.html', {'result': result, 
        'file_url': file_url,
        'patient':patient,
        'diagnosis_patients':Patients.objects.all()})
    
    diagnosis_patients = Patients.objects.all()
    return render(request, 'dermatologist/diagnosis.html', {'diagnosis_patients': diagnosis_patients})

@login_required(login_url='/')
@never_cache
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patients, id=patient_id)
    reports = DiagnosisReport.objects.filter(patient=patient)
    return render(request, 'dermatologist/patientreport.html', {'patient':patient, 'reports': reports})

@login_required(login_url='/')
@never_cache
def diagnose_patient(request, patient_id):
    patient = get_object_or_404(Patients, id=patient_id)
    return render(request, 'dermatologist/diagnosis.html', {'selected_patient':patient})

@login_required(login_url='/')
@never_cache
def send_patient_email(request, patient_id):
    patient = get_object_or_404(Patients, id=patient_id)
    reports = DiagnosisReport.objects.filter(patient=patient)

    #email content
    subject = 'Your Diagnosis Report'
    message = f'Hello {patient.fullname}, \n\nHere are your diagnosis reports:\n'

    for report in reports:
        message += f'\nDiagnosis: {report.result}\nDate: {report.created_at}\n'
        message += f'Image URL: {request.build_absolute_uri(report.image.url)}\n'

    message += '\nBest regards, \nAI DERMATOLOGIST SYSTEM'

    #send the mail
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [patient.email],
        fail_silently=False,
    )

    return redirect('dermatologist/patient_detail', patient_id=patient.id)

def custom_404_view(request, exception):
    render(request, 'dermatologist/pagenotfound.html', status=404)