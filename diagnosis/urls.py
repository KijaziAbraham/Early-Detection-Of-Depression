from django.urls import path
from . import views

urlpatterns = [
    path('patient_details', views.patient_details, name='patient_details'),  

    path('phq9_questionnaire/<int:patient_id>/', views.phq9_questionnaire, name='phq9_questionnaire'),
    path('process_phq9_responses/<int:patient_id>/', views.process_phq9_responses, name='process_phq9_responses'),
    
    path('camera_capture/<int:patient_id>/', views.camera_capture_view, name='camera_capture'),
    path('classify_image/', views.classify_image, name='classify_image'),
    path('result/', views.diagnosis_success_view, name='diagnosis_success'),
    
]
