from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Patients, Profile
from django.core.files.storage import FileSystemStorage
from .model import model, transform
from PIL import Image
import torch

# Create your views here.
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

def index(request):
    return render(request, 'dermatologist/login.html')

def changePassword(request):
    return render(request, 'dermatologist/changePassword.html')

def changepassword2(request):
    return render(request, 'dermatologist/changepassword2.html')

def passwordchangedsuccess(request):
    return render(request, 'dermatologist/passwordchangedsucess.html')

def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user is not None:
            return render(request, 'dermatologist/changepassword2.html', {'username': username})
        else:
            return render(request, 'dermatologist/changePassword.html', {'error': 'Username not found.'})
    return render(request, 'dermatologist/changePassword.html')

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

def graph_analysis(request):
    male_count = Patients.objects.filter(gender='male').count()
    female_count = Patients.objects.filter(gender='female').count()

    context = {
        'male_count':male_count,
        'female_count':female_count,
    }

    return render(request, 'dermatologist/Analytics.html', context)

# register patients view
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
@login_required
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

@login_required
# We changed the variable  name to patientlist from patient  and that was the problem
def patients_list(request):
    patients = Patients.objects.order_by('-registered_date')
    return render(request, 'dermatologist/patients.html', {'patients':patients})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

@login_required 
def dashboard(request):
    total_patients = Patients.objects.count()
    # user_profile = Profile.objects.get(user=request.user)
    return render(request, 'dermatologist/dashboard.html', {'total_patients':total_patients})

def userprofile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'dermatologist/userprofile.html', {'profile':profile})

@login_required
def patients(request):
    return render(request, 'dermatologist/patients.html')

@login_required
def registerPatients(request):
    pass

@login_required
def diagnosis(request):
    diagnosis_patients = Patients.objects.order_by('-registered_date')
    return render(request, 'dermatologist/diagnosis.html', {'diagnosis_patients':diagnosis_patients})

@login_required
def patientsreport(request):
    return render(request, 'dermatologist/patientsreport.html')

@login_required
def Analytics(request):
    return render(request, 'dermatologist/Analytics.html')

def patientreport(request):
    return render(request, 'dermatologist/patientreport.html')

@login_required
def newPatientRegistration(request):
    return render(request, 'dermatologist/newpatientregister.html')

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


# views.py

def classify_image(request):
    if request.method == 'POST' and request.FILES['image-choosed']:
        image = request.FILES['image-choosed']
        patient_id = request.POST['select']
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
                result = "Acne"
            elif predicted.item() == 1:
                result = "Scabies"
            else:
                result = 'Image unrecognized'

        return render(request, 'dermatologist/diagnosis.html', {'result': result, 
        'file_url': file_url,
        'patient':patient,
        'diagnosis_patients':Patients.objects.all()})
    
    diagnosis_patients = Patients.objects.all()
    return render(request, 'dermatologist/diagnosis.html', {'diagnosis_patients': diagnosis_patients})
