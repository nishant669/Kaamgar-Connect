# ═════════════════════════════════════════════════════════════════
# KAAMGAR CONNECT - FORMS
# Reviews, Applications, and Distance Filtering Forms
# ═════════════════════════════════════════════════════════════════

from django import forms
from django.core.exceptions import ValidationError
from reviews.models import Review, ReviewReply
from applications.models import Application
from jobs.models import Job
from workers.models import WorkerProfile


class ReviewForm(forms.ModelForm):
    """Enhanced review form with multi-dimensional ratings"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'quality_rating', 'punctuality', 'communication', 'professionalism']
        widgets = {
            'rating': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Give a title to your review...',
                'required': True,
                'max_length': 200
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your experience with this worker/employer...',
                'rows': 5,
                'required': True,
                'data-maxchars': 1000
            }),
            'quality_rating': forms.HiddenInput(),
            'punctuality': forms.HiddenInput(),
            'communication': forms.HiddenInput(),
            'professionalism': forms.HiddenInput(),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '')
        if len(comment) < 20:
            raise ValidationError('Review must be at least 20 characters long.')
        if len(comment) > 1000:
            raise ValidationError('Review cannot exceed 1000 characters.')
        return comment


class ReviewReplyForm(forms.ModelForm):
    """Form for replying to reviews"""
    
    class Meta:
        model = ReviewReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your reply...',
                'rows': 3,
                'required': True,
                'max_length': 500
            })
        }

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message) < 10:
            raise ValidationError('Reply must be at least 10 characters long.')
        return message


class DistanceFilterForm(forms.Form):
    """Form for distance-based job/worker filtering"""
    
    RADIUS_CHOICES = [
        (5, '5 km'),
        (10, '10 km'),
        (15, '15 km'),
        (20, '20 km'),
        (25, '25 km'),
        (50, '50 km'),
        (100, '100 km'),
    ]
    
    radius = forms.ChoiceField(
        choices=RADIUS_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        initial=10,
        label='Select search radius'
    )
    use_my_location = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Use my current location'
    )


class JobFilterForm(forms.Form):
    """Advanced job filtering form with distance support"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search job titles, keywords...',
        })
    )
    
    category = forms.MultipleChoiceField(
        required=False,
        choices=Job.JOB_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    )
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter location...',
        })
    )
    
    salary_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Minimum salary',
            'type': 'number',
        })
    )
    
    salary_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Maximum salary',
            'type': 'number',
        })
    )
    
    job_type = forms.MultipleChoiceField(
        required=False,
        choices=Job.JOB_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    )
    
    experience = forms.MultipleChoiceField(
        required=False,
        choices=Job.EXPERIENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    )
    
    distance_radius = forms.IntegerField(
        required=False,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-range',
            'type': 'range',
            'min': '1',
            'max': '100',
            'step': '1',
            'placeholder': 'Distance (km)',
        })
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', 'Newest'),
            ('-salary_max', 'Highest Salary'),
            ('salary_min', 'Lowest Salary'),
            ('-is_featured', 'Featured First'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )


class WorkerFilterForm(forms.Form):
    """Form for filtering workers with distance support"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search worker names, skills...',
        })
    )
    
    skills = forms.MultipleChoiceField(
        required=False,
        choices=WorkerProfile.SKILL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
        })
    )
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter location...',
        })
    )
    
    min_rating = forms.FloatField(
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-range',
            'type': 'range',
            'min': '0',
            'max': '5',
            'step': '0.5',
            'placeholder': 'Minimum rating',
        })
    )
    
    min_experience = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '0',
            'placeholder': 'Minimum experience (years)',
        })
    )
    
    max_daily_rate = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'type': 'number',
            'min': '0',
            'placeholder': 'Maximum daily rate',
        })
    )
    
    available_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Available workers only'
    )
    
    verified_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Verified workers only'
    )
    
    distance_radius = forms.IntegerField(
        required=False,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-range',
            'type': 'range',
            'min': '1',
            'max': '100',
            'step': '1',
            'placeholder': 'Distance (km)',
        })
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('-rating', 'Highest Rated'),
            ('-total_jobs', 'Most Jobs Completed'),
            ('daily_rate', 'Lowest Rate'),
            ('-daily_rate', 'Highest Rate'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )


class ApplicationReviewForm(forms.Form):
    """Form for employers to accept applications and request review from workers"""
    
    action = forms.ChoiceField(
        choices=[
            ('shortlist', 'Shortlist'),
            ('accept', 'Accept'),
            ('reject', 'Reject'),
        ],
        widget=forms.HiddenInput()
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Add a message to the worker...',
            'rows': 3,
        })
    )
    
    request_review = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        label='Request worker to leave a review after work completion'
    )


class WorkerApplicationActionForm(forms.Form):
    """Form for workers to respond to job applications"""
    
    action = forms.ChoiceField(
        choices=[
            ('accept', 'Accept Job'),
            ('reject', 'Reject Job'),
            ('negotiate', 'Negotiate'),
        ],
        widget=forms.HiddenInput()
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Add a message to the employer...',
            'rows': 3,
        })
    )
    
    proposed_rate = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Proposed daily rate (for negotiation)',
            'type': 'number',
            'step': '100',
            'min': '0',
        })
    )
