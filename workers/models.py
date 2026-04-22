from django.db import models
from django.conf import settings
from math import radians, sin, cos, sqrt, atan2

SKILL_CHOICES = [
    ('plumber','Plumber'),('electrician','Electrician'),
    ('carpenter','Carpenter'),('painter','Painter'),
    ('driver','Driver'),('cook','Cook'),
    ('security','Security Guard'),('cleaner','Cleaner'),
    ('mason','Mason'),('welder','Welder'),
    ('ac_technician','AC Technician'),('tailor','Tailor'),
    ('other','Other'),
]

class WorkerProfile(models.Model):
    SKILL_CHOICES = SKILL_CHOICES
    user              = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='worker_profile')
    skills            = models.CharField(max_length=50, choices=SKILL_CHOICES, default='other')
    extra_skills      = models.CharField(max_length=300, blank=True, help_text='Additional comma-separated skills')
    experience_years  = models.PositiveIntegerField(default=0)
    daily_rate        = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    availability      = models.BooleanField(default=True)
    rating            = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    total_jobs        = models.PositiveIntegerField(default=0)
    address           = models.TextField(blank=True)
    latitude          = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Worker location latitude')
    longitude         = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Worker location longitude')
    working_radius_km = models.PositiveIntegerField(default=10, help_text='Working radius in kilometers')
    resume            = models.FileField(upload_to='worker_resumes/', blank=True, null=True)
    aadhar_verified   = models.BooleanField(default=False)
    portfolio_url     = models.URLField(blank=True)
    languages         = models.CharField(max_length=200, blank=True, default='Hindi, English')
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.skills}"

    def completion_pct(self):
        checks = [
            bool(self.user.first_name),
            bool(self.user.phone),
            bool(self.user.bio),
            bool(self.user.profile_photo),
            bool(self.daily_rate),
            bool(self.experience_years),
            bool(self.address),
            bool(self.resume),
            bool(self.aadhar_verified),
            bool(self.extra_skills),
        ]
        return int(sum(checks) / len(checks) * 100)

    def extra_skills_list(self):
        return [s.strip() for s in self.extra_skills.split(',') if s.strip()]

    def distance_to(self, other_lat, other_lon):
        """Calculate distance in kilometers using Haversine formula"""
        if not self.latitude or not self.longitude:
            return None
        
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        lat1, lon1 = radians(float(self.latitude)), radians(float(self.longitude))
        lat2, lon2 = radians(float(other_lat)), radians(float(other_lon))
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return round(R * c, 2)

    def is_within_radius(self, other_lat, other_lon):
        """Check if location is within working radius"""
        distance = self.distance_to(other_lat, other_lon)
        if distance is None:
            return True  # Accept if no coordinates set
        return distance <= self.working_radius_km
