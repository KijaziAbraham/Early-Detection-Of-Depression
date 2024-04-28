from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.core.validators import RegexValidator


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    middle_name = forms.CharField(max_length=30, required=False )
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    license_number = forms.CharField(max_length=15, required=True, help_text='Required. Enter your valid license number.')

    phone_number = forms.CharField(max_length=17, required=True,
        
        help_text="Phone number must be entered in the format: '+255628592577 or 0628592577'. Up to 15 digits allowed."
    )

    qualification = forms.CharField(max_length=100, required=True, help_text='Required. Enter your qualification.')

    QUALIFICATION_CHOICES = [
        ('clinical_officer', 'Clinical Officer'),
        ('medical_doctor', 'Medical Doctor'),
    ]

    qualification = forms.ChoiceField(choices=QUALIFICATION_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'middle_name','last_name', 'license_number', 'phone_number', 'qualification', 'password1', 'password2')
    
    def clean_license_number(self):
        data = self.cleaned_data['license_number']
        # Add your own validation for the license number
        if not data.startswith('MCT'):
            raise forms.ValidationError("License number must start with MCT")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # Assuming you have a field for the license number in your CustomUser model
        user.license_number = self.cleaned_data['license_number']
        if commit:
            user.save()
        return user
    
    def clean_phone_number(self):
        phone_no = self.cleaned_data['phone_number']
        if not phone_no.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_no) < 10 or len(phone_no) > 15:
            raise forms.ValidationError("Phone number must be between 10 and 15 digits.")
        return phone_no


    # def clean_email(self):
