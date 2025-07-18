from django.urls import path
from django.conf.urls import handler404
from ai_dermatologist import views

handler404 = views.custom_404_view

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_password/', views.Update_password, name='update_password'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('changepassword2/', views.changepassword2, name='changepassword2'),
    path('passwordchangedsucess/', views.passwordchangedsuccess, name='passwordchangedsuccess'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('patients/', views.patients, name='patients'),
    path('patientsreport/', views.patientsreport, name='patientsreport'),
    path('patientreport/', views.patientreport, name='patientreport'),
    path('analytics/', views.Analytics, name='analytics'),
    path('register/', views.register, name='register'),
    path('patientslist/', views.patients_list, name='patientslist'),
    path('newpatientregistration/', views.newPatientRegistration, name='newpatientregistration'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('update_user/', views.update_user, name='update_user'),
    path('classify/', views.classify_image, name='classify_image'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('diagnose/<int:patient_id>/', views.diagnose_patient, name='diagnose_patient'),
    path('send_email/<int:patient_id>/', views.send_patient_email, name='send_patient_email'),
    # path('report/', views.diagnosis_reports, name='diagnosis_reports'),
    # path('diagnosed_patient_reports/', views.diagnosed_patient_reports, name='diagnosed_patients_report'),
    # path('count_report/', views.count_reports, name='count_reports'),
]