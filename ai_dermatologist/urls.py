from django.urls import path
from ai_dermatologist import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_password/', views.Update_password, name='update_password'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('changepassword2/', views.changepassword2, name='changepassword2'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('patients/', views.patients, name='patients'),
    path('patientsreport/', views.patientsreport, name='patientsreport'),
    path('patientreport/', views.patientreport, name='patientreport'),
    path('analytics/', views.Analytics, name='analytics'),
    path('register/', views.register, name='register'),
    path('patientslist/', views.patients_list, name='patientslist'),
    path('newpatientregistration/', views.newPatientRegistration, name='newpatientregistration')
]