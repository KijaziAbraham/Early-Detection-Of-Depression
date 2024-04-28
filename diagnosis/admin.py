from django.contrib import admin
from .models import PHQ9Question
from .models import DiagnosedPatient

class PHQ9QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'option_1', 'option_2', 'option_3', 'option_4']

admin.site.register(PHQ9Question, PHQ9QuestionAdmin)


class DiagnosedPatientAdmin(admin.ModelAdmin):
    list_display =['full_name', 'age', 'address', 'sex' ]

admin.site.register(DiagnosedPatient, DiagnosedPatientAdmin)
