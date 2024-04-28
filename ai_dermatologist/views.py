from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Patients

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

def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user is not None:
            return render(request, 'changepassword2.html', {'username': username})
        else:
            return render(request, 'changePassword.html', {'error': 'Username not found.'})
    return render(request, 'changePassword.html')

def Update_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user is not None:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_success')
        else:
            return render(request, 'changePassword.html', {'error': 'username not found'})
    return redirect('changePassword')

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
        render(request, 'patientslist.html')

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
    return render(request, 'dermatologist/dashboard.html', {'total_patients':total_patients})

@login_required
def patients(request):
    return render(request, 'dermatologist/patients.html')

@login_required
def registerPatients(request):
    pass

@login_required
def diagnosis(request):
    return render(request, 'dermatologist/diagnosis.html')

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

