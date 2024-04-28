# forms.py
from django import forms
from .models import DiagnosedPatient

class PatientDetailsForm(forms.ModelForm):
    class Meta:
        model = DiagnosedPatient
        fields = ['first_name', 'middle_name', 'last_name', 'age', 'address', 'sex']
