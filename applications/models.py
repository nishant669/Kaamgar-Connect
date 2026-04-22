from django.db import models
from django.conf import settings
from jobs.models import Job
STATUS_CHOICES = [
    ('pending','Pending'),('reviewed','Reviewed'),
    ('shortlisted','Shortlisted'),('accepted','Accepted'),('rejected','Rejected'),
]

class Application(models.Model):
    job        = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    worker     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cover_note = models.TextField(blank=True)
    resume     = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'worker')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.worker.username} → {self.job.title} [{self.status}]"

    def status_color(self):
        colors = {'pending':'amber','reviewed':'blue','shortlisted':'purple','accepted':'green','rejected':'red'}
        return colors.get(self.status, 'gray')


class WorkerReview(models.Model):

    worker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="worker_reviews"
    )

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    review = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.worker} - {self.rating}⭐"