from django import forms
from django.forms import CheckboxInput, DateInput, ModelForm, NumberInput, Select, SelectMultiple, TextInput, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from itsdangerous import exc
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username"}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}))

# Create a Hospital User
class HospitalUserForm(UserCreationForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder":"Email"}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username"}))
    password1 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}))
    password2 = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    # def save(self, *args, commit=True):
    #     try:
    #         user = super().save(commit=False)

    #         user.username = self.cleaned_data['username']
    #         user.email = self.cleaned_data['email']
    #         user.first_name = self.cleaned_data['first_name']
    #         user.last_name = self.cleaned_data['last_name']
    #         user.password1 = self.cleaned_data['password1']

    #         if commit:
    #             user.save()
    #         return user
    #     except:
    #         print ("Error")



class HospitalUserRolesForm(forms.ModelForm):
    User_Type = [
        ('Doctor', "DOCTOR"),
        ('Nurse', "NURSE"),
        ('Receptionist', "RECEPTIONIST"),
    ]
    # role = forms.CharField(max_length=100, choices= User_Type)

    class Meta:
        model = HospitalUser
        fields = ('role',)
        widgets= {
            'role': Select(attrs={'class': 'form-control', "placeholder": "Type of User"})
            }

# class DeleteUser(forms.Form):
#     email = forms.EmailField(required = True, widget=forms.EmailInput(attrs={'class': 'form-control', "placeholder":"Email"}))


class PatientBioForm(forms.ModelForm):
    #Patient Bio Info
    # firstname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    # lastname = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    # dob = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}))
    # gender = forms.CharField(widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}, choices = gender_choices))
    # nationality = forms.CharField(max_length=400, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nationality'}))

    class Meta:
        model = PatientBio
        fields = ['firstname', 'lastname', 'dob', 'gender', 'nationality']
        widgets = {
            'firstname': TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}),
            'lastname': TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
            'dob': DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'gender': Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}, choices = PatientBio.gender_choices),
            'nationality': TextInput(attrs={'class': 'form-control', 'placeholder':'Nationality'})
        }

class PatientVitalsForm(forms.ModelForm):
    #Patient Vitals
    # temperature = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Patient Temperature(Degrees Celsius)'}))
    # weight = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Patient Weight'}))

    class Meta:
        model = PatientVitals
        fields = ['bio', 'temperature', 'weight']
        widgets = {
            'temperature': NumberInput(attrs={'class': 'form-control', 'placeholder':'Patient Temperature(Degrees Celsius)'}),
            'weight': NumberInput(attrs={'class': 'form-control', 'placeholder':'Patient Weight'})
        }


class PatientDiagnosticForm(forms.ModelForm):
    #Patient Diagnostic
    diagnostic = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Diagnostic'}))
    treatment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Treatment'}))

    class Meta:
        model = PatientDiagnoses
        fields = ('patient', 'diagnostic', 'treatment')
