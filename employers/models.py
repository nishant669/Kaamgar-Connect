from django.db import models
from django.conf import settings

class Employer(models.Model):
    user         = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website      = models.URLField(blank=True)
    industry     = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True, choices=[
        ('1-10','1-10 employees'),('11-50','11-50 employees'),
        ('51-200','51-200 employees'),('200+','200+ employees'),
    ])
    description  = models.TextField(blank=True)
    location     = models.CharField(max_length=200, blank=True)
    established  = models.PositiveIntegerField(null=True, blank=True)
    verified     = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name or self.user.username

    @property
    def total_jobs(self):
        return self.user.posted_jobs.count()

    @property 
    def active_jobs(self):
        return self.user.posted_jobs.filter(is_active=True).count()
