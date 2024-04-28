from django.shortcuts import render, redirect
from .forms import PatientDetailsForm
from .models import DiagnosedPatient, PHQ9Question, PHQ9Response
from user_authentication.models import CustomUser
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db import models
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from diagnosis.models import DiagnosedPatient
from django.shortcuts import render, redirect
from django.http import JsonResponse
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from django.db.models import Sum
from tensorflow.keras.models import load_model


def patient_details(request):
    if request.method == 'POST':
        form = PatientDetailsForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            return redirect('phq9_questionnaire', patient_id=patient.id)  # Redirect to PHQ-9 questionnaire with patient ID
    else:
        form = PatientDetailsForm()
    return render(request, 'diagnosis/patient_details.html', {'form': form})

from django.shortcuts import render, redirect

def phq9_questionnaire(request, patient_id):
    patient = DiagnosedPatient.objects.get(id=patient_id)
    questions = PHQ9Question.objects.all()
    if request.method == 'POST':
        # If the form is submitted, redirect to the processing view
        return redirect('process_phq9_responses', patient_id=patient_id)
    # If the request is GET, render the questionnaire page
    return render(request, 'diagnosis/phq9_questionnaire.html', {'patient': patient, 'questions': questions})


def process_phq9_responses(request, patient_id):
    patient = DiagnosedPatient.objects.get(id=patient_id)
    if request.method == 'POST':
        total_score = 0  # Initialize total score
        for question_id, response in request.POST.items():
            if question_id.startswith('phq'):
                question = PHQ9Question.objects.get(pk=question_id[3:])
                try:
                    PHQ9Response.objects.create(
                        user=request.user,
                        patient=patient,
                        question=question,
                        response=int(response)
                    )
                    total_score += int(response)  # Add response to total score
                except IntegrityError as e:
                    return HttpResponse("An error occurred while processing the responses.")

        # Determine diagnosis based on total score
        diagnosis_result = determine_diagnosis(total_score)
        patient.diagnosis_result = diagnosis_result
        patient.save()
        return redirect('camera_capture', patient_id=patient.id)

  
def determine_diagnosis(total_score):
    if total_score <= 4:
        return "No depression"
    elif total_score <= 9:
        return "Mild depression"
    elif total_score <= 14:
        return "Moderate depression"
    elif total_score <= 19:
        return "Moderately severe depression"
    else:
        return "Severe depression"












# Assuming the model is loaded here for simplicity; consider using a better strategy for production
model = load_model('diagnosis/models/imageclassifiernewlive.h5')


from django.urls import reverse

def camera_capture_view(request, patient_id):
    patient = DiagnosedPatient.objects.get(id=patient_id)
    context = {'patient': patient}
    return render(request, 'diagnosis/camera_capture.html', context)




def classify_image(request):
    if request.method == 'POST' and request.POST.get('image'):
        try:
            # Decode the image from Base64 and convert to PIL Image
            image_data = request.POST.get('image').split(',')[1]
            image_bytes = base64.b64decode(image_data)
            image_pil = Image.open(BytesIO(image_bytes))
            image_pil = image_pil.resize((256, 256))

            # Convert to NumPy array and normalize
            image_np = np.array(image_pil) / 255.0
            image_np = np.expand_dims(image_np, axis=0)

            # Predict using the model
            predictions = model.predict(image_np)
            predicted_class_index = np.argmax(predictions)

            # Map predicted index to string
            class_map = {0: "Happy", 1: "Sad"}
            predicted_class_label = class_map.get(predicted_class_index, "Unknown")

            # Return the predicted class label
            return JsonResponse({'predicted_class_label': predicted_class_label})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'This endpoint only supports POST requests.'}, status=405)





def diagnosis_success_view(request):
    predicted_class_label = request.GET.get('label', 'Unknown')
    patient_id = request.GET.get('patient_id')  # Retrieve patient_id from URL parameters

    # Retrieve the patient object using the patient_id
    patient = get_object_or_404(DiagnosedPatient, id=patient_id)

    return render(request, 'diagnosis/diagnosis_success.html', {'predicted_class_label': predicted_class_label, 'patient': patient})







