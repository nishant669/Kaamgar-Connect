from django.contrib.auth.models import AbstractUser
from django.db import models
import random, string

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('worker', 'Worker'), ('employer', 'Employer')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')
    phone = models.CharField(max_length=15, blank=True)
    otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=5, default='en', choices=[('en','English'),('hi','Hindi')])
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.save()
        return self.otp

    def __str__(self):
        return f"{self.username} ({self.role})"
