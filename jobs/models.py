from django.db import models
from django.conf import settings
from math import radians, sin, cos, sqrt, atan2

JOB_CATEGORY_CHOICES = [
    ('construction','Construction'),('electrical','Electrical'),
    ('plumbing','Plumbing'),('carpentry','Carpentry'),
    ('painting','Painting'),('driving','Driving'),
    ('cooking','Cooking'),('cleaning','Cleaning'),
    ('security','Security'),('welding','Welding'),
    ('ac_tech','AC Technician'),('tailoring','Tailoring'),
    ('other','Other'),
]
JOB_TYPE_CHOICES = [
    ('full_time','Full Time'),('part_time','Part Time'),
    ('contract','Contract'),('daily','Daily Wage'),
    ('internship','Internship'),
]
EXPERIENCE_CHOICES = [
    ('fresher','Fresher (0 yrs)'),('1_2','1–2 Years'),
    ('3_5','3–5 Years'),('5_plus','5+ Years'),
    ('10_plus','10+ Years'),
]

class Job(models.Model):
    JOB_CATEGORY_CHOICES = JOB_CATEGORY_CHOICES
    employer        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    title           = models.CharField(max_length=200)
    title_hi        = models.CharField(max_length=200, blank=True)
    category        = models.CharField(max_length=30, choices=JOB_CATEGORY_CHOICES)
    job_type        = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_req  = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    skills_required = models.CharField(max_length=500, blank=True, help_text='Comma-separated skills')
    description     = models.TextField()
    description_hi  = models.TextField(blank=True)
    location        = models.CharField(max_length=200)
    latitude        = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Job location latitude')
    longitude       = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, help_text='Job location longitude')
    salary_min      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salary_max      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    openings        = models.PositiveIntegerField(default=1)
    is_active       = models.BooleanField(default=True)
    is_featured     = models.BooleanField(default=False)
    views           = models.PositiveIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deadline        = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def skills_list(self):
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]

    def category_icon(self):
        icons = {
            'construction':'🏗️','electrical':'⚡','plumbing':'🔧',
            'carpentry':'🪚','painting':'🎨','driving':'🚗',
            'cooking':'👨‍🍳','cleaning':'🧹','security':'🛡️',
            'welding':'⚒️','ac_tech':'❄️','tailoring':'🧵','other':'💼',
        }
        return icons.get(self.category, '💼')

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


class SavedJob(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_jobs')
    job        = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saves')
    saved_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
