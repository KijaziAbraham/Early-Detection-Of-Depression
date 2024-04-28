from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    # Adding a phone number field with validation
   
    phone_number = models.CharField( max_length=17, blank=False)

    # Adding a license number field, unique to ensure no two users can share the same license number
    license_number = models.CharField(max_length=20, unique=True)

    # Optional: Add a field to store profile images
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.license_number})"
