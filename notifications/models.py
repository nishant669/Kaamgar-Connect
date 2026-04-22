from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPES = [
        ('application', 'New Application'),
        ('status',      'Application Status Changed'),
        ('message',     'New Message'),
        ('review',      'New Review'),
        ('job',         'New Job Match'),
    ]
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    ntype      = models.CharField(max_length=20, choices=TYPES)
    title      = models.CharField(max_length=200)
    body       = models.TextField(blank=True)
    link       = models.CharField(max_length=300, blank=True)
    is_read    = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.title}'
