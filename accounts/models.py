from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random


class CustomUser(AbstractUser):
    ROLE_CHOICES = [('worker', 'Worker'), ('employer', 'Employer')]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')
    phone = models.CharField(max_length=15, blank=True)

    otp = models.CharField(max_length=6, blank=True)
    otp_verified = models.BooleanField(default=False)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    language = models.CharField(max_length=5, default='en', choices=[('en','English'),('hi','Hindi')])
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔐 Generate OTP
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.otp_verified = False
        self.save()
        return self.otp

    # 🔐 Verify OTP (single source of truth)
    def verify_otp(self, input_otp):
        if self.otp != input_otp:
            return False

        if not self.otp_created_at:
            return False

        if timezone.now() > self.otp_created_at + timedelta(minutes=5):
            return False

        self.otp_verified = True
        self.otp = ''
        self.save()
        return True

    def __str__(self):
        return f"{self.username} ({self.role})"