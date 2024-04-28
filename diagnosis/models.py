# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class DiagnosedPatient(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    sex_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
       
    ]
    sex = models.CharField(max_length=1, choices=sex_choices)
    # Add other fields as needed
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"





class PHQ9Question(models.Model):
    question_text = models.CharField(max_length=200)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)

class PHQ9Response(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey(DiagnosedPatient, on_delete=models.CASCADE)  
    question = models.ForeignKey(PHQ9Question, on_delete=models.CASCADE)
    response = models.IntegerField()
    

   