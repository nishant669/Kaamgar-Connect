from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

RATING_CHOICES = [
    (5, '⭐⭐⭐⭐⭐ Excellent'),
    (4, '⭐⭐⭐⭐ Very Good'),
    (3, '⭐⭐⭐ Good'),
    (2, '⭐⭐ Fair'),
    (1, '⭐ Poor'),
]

class Review(models.Model):
    RATING_CHOICES = RATING_CHOICES
    reviewer        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reviews')
    job             = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    application     = models.OneToOneField('applications.Application', on_delete=models.CASCADE, related_name='review', null=True, blank=True)
    rating          = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATING_CHOICES)
    title           = models.CharField(max_length=200, blank=True, help_text='Review title')
    comment         = models.TextField(blank=True, help_text='Detailed feedback')
    
    # Rating dimensions
    quality_rating  = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5, help_text='Quality of work')
    punctuality     = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5, help_text='On-time delivery')
    communication   = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5, help_text='Communication skill')
    professionalism = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5, help_text='Professional behavior')
    
    is_verified     = models.BooleanField(default=False, help_text='Verified purchase/work')
    is_featured     = models.BooleanField(default=False)
    helpful_count   = models.PositiveIntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('reviewer', 'reviewee', 'job')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reviewee', '-created_at']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f'{self.reviewer.username} → {self.reviewee.username}: {self.rating}★'

    @property
    def average_rating(self):
        return round((self.quality_rating + self.punctuality + self.communication + self.professionalism) / 4, 1)

    @property
    def rating_display(self):
        return dict(self.RATING_CHOICES).get(self.rating, f'{self.rating}★')


class ReviewReply(models.Model):
    """Allow reviewee to reply to reviews"""
    review          = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='reply')
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply to {self.review.id} by {self.author.username}"

    class Meta:
        ordering = ['created_at']
