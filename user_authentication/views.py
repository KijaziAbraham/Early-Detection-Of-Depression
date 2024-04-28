from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm  # Use Django's built-in form for authentication
from .forms import CustomUserCreationForm
from django.contrib import messages

# Registration View
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the newly created user
            messages.success(request, 'Registration successful! You are now logged in.')
            # Redirect to a homepage or profile page after successful registration
            return redirect('login')  # Replace 'homepage' with your actual URL name
        else:
            # If the form is not valid, show the form again with errors
            messages.error(request, 'Registration failed. Please correct the errors below.')
            return render(request, 'user_authentication/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_authentication/register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful! Welcome back.')
                return redirect('patient_details')  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid login details.')
    else:
        form = AuthenticationForm()
    return render(request, 'user_authentication/login.html', {'form': form})





