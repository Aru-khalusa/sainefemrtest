from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    # Patient Info
    path('patient/', views.patientBio, name='patient'),
    path('patient/update/<int:pk>', views.patientBioUpdate, name='patient-update'),
    path('patient/delete/<int:pk>', views.patientBioDelete, name='patient-delete'),
    path('patient/restore/<int:pk>', views.patientBioRestore, name='patient-restore'),
    path('patient/all', views.patientBioArchive, name='patient-all'),
    # vitals
    path('vitals/', views.patientVitals, name='vitals'),
    path('vitals/update/<bio_id>', views.patientVitalsUpdate, name='vitals-update'),
    path('vitals/delete/<bio_id>', views.patientVitalsDelete, name='vitals-delete'),
    path('vitals/restore/<bio_id>', views.patientVitalsRestore, name='vitals-restore'),
    path('vitals/', views.patientVitalsArchive, name='vitals-all'),
    # diagnosis
    path('diagnosis/', views.patientDiagnose, name='diagnose'),
    path('diagnosis/update/<patient_id>', views.patientDiagnoseUpdate, name='diagnosis-update'),
    path('diagnosis/delete/<patient_id>', views.patientDiagnoseDelete, name='diagnosis-delete'),
    path('diagnosis/restore/<patient_id>', views.patientDiagnoseRestore, name='diagnosis-restore'),
    path('diagnosis/all', views.patientDiagnoseArchive, name='diagnose-all'),
    # logout
    path('logout/', views.logout_user, name='logout'),
]