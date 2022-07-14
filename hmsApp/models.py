import email
from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

# class User(AbstractUser):
#     email = models.EmailField(unique=True)

#     USER

class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True



class HospitalUser(models.Model):
    User_Type = [
        ('Doctor', "DOCTOR"),
        ('Nurse', "NURSE"),
        ('Receptionist', "RECEPTIONIST"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200, choices=User_Type)

    def __str__(self):
        return self.user.username

class PatientBio(SoftDelete):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    firstname = models.CharField(max_length=200, verbose_name="Patient First Name")
    lastname = models.CharField(max_length=200, verbose_name="Patient Last Name")
    dob = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=200, choices = gender_choices, verbose_name="Gender")
    nationality = models.CharField(max_length=200, verbose_name="Nationality")

    def __str__(self):
        return self.firstname + " " + self.lastname + " " + str(self.dob)

class PatientVitals(SoftDelete):
    bio = models.ForeignKey(PatientBio, on_delete=models.CASCADE)
    temperature = models.IntegerField(verbose_name="Temperature")
    weight = models.IntegerField(verbose_name="Weight")

    def __str__(self):
        return "Vitals of " + str(self.bio.firstname) + " " + str(self.bio.lastname)

class PatientDiagnoses(SoftDelete):
    patient = models.ForeignKey(PatientVitals, on_delete=models.CASCADE)
    diagnostic = models.TextField(verbose_name="Diagnosis")
    treatment = models.TextField(verbose_name="Treatment")

    def __str__(self):
        return "Diagnoses and Treatment for " + str(self.patient.bio.firstname) + " " + str(self.patient.bio.lastname)


