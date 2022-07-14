from re import template
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import *
from .models import *

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
      
        if user is not None and user.is_superuser and user.is_staff:
            login(request, user)
            return redirect(to='patient')
        elif user is not None and user.is_staff and not user.is_superuser:
            login(request, user)
            return redirect(to='vitals')
        elif user is not None:
            login(request, user)
            return redirect(to='diagnose')
        else:
            return redirect(to='login')
    else:
        pass


    return render(request, "hmsApp/login.html")
       

@login_required
def patientBio(request):
    form = PatientBioForm(request.POST)
    patients = PatientBio.objects.filter(is_deleted=False)

    # if 'search' in request.GET:
    #     search = request.GET['search']
    #     multi_search = Q(Q(firstname__icontains=search) | Q(lastname__icontains=search) | Q(dob__icontains=search) | Q(gender__icontains=search) | Q(nationality__icontains=search))
    #     PatientBio.objects.filter(multi_search)
    # else: 
    #     patients = PatientBio.objects.filter(is_deleted=False)

    if form.is_valid():
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        dob = form.cleaned_data['dob']
        gender = form.cleaned_data['gender']
        nationality = form.cleaned_data['nationality']
        PatientBio.objects.create(firstname=firstname, lastname=lastname, dob=dob, gender=gender, nationality=nationality)

        msg = messages.success(request, "Patient Added Successfully")
        return redirect(to='patient')
    else:
        form = PatientBioForm(request.POST)

    
    context = {
        'form': form,
        'patients': patients,

    }

    return render(request, 'hmsApp/receptionist.html', context)

@login_required    
def patientBioUpdate(request, pk):
    patients = PatientBio.objects.get(id=pk)
    form = PatientBioForm(request.POST or None, instance=patients)

    if form.is_valid():
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        dob = form.cleaned_data['dob']
        gender = form.cleaned_data['gender']
        nationality = form.cleaned_data['nationality']
        patients.firstname =firstname
        patients.lastname =lastname
        patients.dob =dob
        patients.gender =gender
        patients.nationality =nationality
        patients.save()

        msg = messages.success(request, "Patient Updated Successfully")
        return redirect(to='patient')
    else:
        form = PatientBioForm(request.POST)
    
    context = {
        'form': form,
        'patients': patients,

    }

    return render(request, 'hmsApp/receptionist-update.html', context)

@login_required
def patientBioDelete(request, pk):
    patient = PatientBio.objects.get(id=pk)
    patient.soft_delete()
    return redirect(to='patient')

@login_required
def patientBioRestore(request, pk):
    patients = PatientBio.objects.get(id=pk)
    patients.restore()
    return redirect(to='patient')


def patientBioArchive(request):
    patients = PatientBio.objects.all()

    return render(request, 'hmsApp/receptionist-restore.html', {'patients': patients})

@login_required
def patientVitals(request):
    form = PatientVitalsForm(request.POST)
    patients = PatientBio.objects.filter(is_deleted=False)
    vitals = PatientVitals.objects.filter(is_deleted=False)
    viewAll = PatientVitals.objects.all()

    if form.is_valid():
        bio = form.cleaned_data['bio']
        weight = form.cleaned_data['weight']
        temperature = form.cleaned_data['temperature']
        PatientVitals.objects.create(bio=bio, weight=weight, temperature=temperature)
        msg = messages.success(request, "Vitals for {{bio.firstname}} Added Successfully")
        return redirect(to='vitals')
    else:
        PatientVitalsForm(request.POST)

    context = {
        'form': form,
        'patients': patients,
        'vitals': vitals,
        'restore': viewAll,
    }

    return render(request, 'hmsApp/nurse.html', context)

@login_required
def patientVitalsUpdate(request, bio_id):
    vitals = PatientVitals.objects.get(pk=bio_id)
    form = PatientVitalsForm(request.POST, instance=vitals)

    if form.is_valid():
        weight = form.cleaned_data['weight']
        temperature = form.cleaned_data['temperature']
        
        vitals.weight =weight
        vitals.temperature =temperature
        vitals.save()

        msg = messages.success(request, "Patient Vitals Updated Successfully")
        return redirect(to='vitals')
    else:
        form = PatientVitalsForm(request.POST)
        messages.error(request, "Vitals Not Updated")
    
    context = {
        'form': form,
        'vitals': vitals,
    }

    return render(request, 'hmsApp/nurse-update.html', context)

@login_required
def patientVitalsDelete(request, bio_id):
    vitals = PatientVitals.objects.get(pk=bio_id)
    vitals.soft_delete()
    return redirect(to='vitals')

@login_required
def patientVitalsRestore(request, bio_id):
    vitals = PatientVitals.objects.get(pk=bio_id)
    vitals.restore()

    return redirect(to='vitals')

@login_required
def patientVitalsArchive(request):
    vitals = PatientBio.objects.all()

    return render(request, 'hmsApp/nurse-restore.html', {'vitals': vitals})

@login_required
def patientDiagnose(request):
    form = PatientDiagnosticForm(request.POST)
    patients = PatientBio.objects.filter(is_deleted=False)
    diagnoses = PatientDiagnoses.objects.filter(is_deleted=False)

    if form.is_valid():
        patient = form.cleaned_data['patient']
        diagnostic = form.cleaned_data['diagnostic']
        treatment = form.cleaned_data['treatment']
        PatientDiagnoses.objects.create(patient=patient, diagnostic=diagnostic, treatment=treatment)
        msg = messages.success(request, "Patient {{patient.bio.id}} Diagnosed Successfully")
        return redirect(to='diagnose')
    else:
        PatientDiagnosticForm(request.POST)

    context = {
        'form': form,
        'patients': patients,
        'diagnoses': diagnoses,
    }

    return render(request, 'hmsApp/doctor.html', context)

@login_required
def patientDiagnoseUpdate(request, patient_id):
    diagnoses = PatientDiagnoses.objects.get(pk=patient_id)
    form = PatientDiagnosticForm(request.POST, instance=diagnoses)


    if request.method=='POST':
        if form.is_valid():
            diagnostic = form.cleaned_data['diagnostic']
            treatment = form.cleaned_data['treatment']
            diagnoses.diagnostic = diagnostic
            diagnoses.treatment = treatment
            diagnoses.save()
            msg = messages.success(request, "Patient {{patients.firstname}} Diagnosis Updated Successfully")
            return redirect(to='diagnose')
        else:
            form = PatientDiagnosticForm(request.POST)

    context = {
        'form': form,
        'diagnosis': diagnoses,
    }

    return render(request, 'hmsApp/doctor-update.html', context)


@login_required
def patientDiagnoseDelete(request, patient_id):
    diagnose = PatientDiagnoses.objects.get(pk=patient_id)
    diagnose.soft_delete()
    return redirect(to='diagnose')


@login_required
def patientDiagnoseRestore(request, patient_id):
    diagnoses = PatientDiagnoses.objects.get(pk=patient_id)
    diagnoses.restore()

    return redirect(to='diagnose')

@login_required
def patientDiagnoseArchive(request):
    diagnoses = PatientDiagnoses.objects.all()

    return render(request, 'hmsApp/doctor-restore.html', {'diagnoses': diagnoses})

@login_required
def logout_user (request):
    logout(request)
    return redirect(to='login')
