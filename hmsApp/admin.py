from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(HospitalUser)
admin.site.register(PatientBio)
admin.site.register(PatientVitals)
admin.site.register(PatientDiagnoses) 
