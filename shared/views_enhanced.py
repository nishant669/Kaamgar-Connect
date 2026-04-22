# ═════════════════════════════════════════════════════════════════
# KAAMGAR CONNECT - ENHANCED VIEWS FOR REVIEWS & DISTANCE FILTERING
# Add to respective app views or create new review/distance views
# ═════════════════════════════════════════════════════════════════

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg, Count
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from reviews.models import Review, ReviewReply
from applications.models import Application
from jobs.models import Job
from workers.models import WorkerProfile
from decimal import Decimal
import math

# ═════════════════════════════════════════════════════════════════
# REVIEW SYSTEM VIEWS
# ═════════════════════════════════════════════════════════════════

@login_required
@require_http_methods(["POST"])
def submit_review(request, application_id):
    """Submit a review for a completed job"""
    application = get_object_or_404(Application, id=application_id)
    
    # Only the person who hired can leave review
    if request.user != application.job.employer:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    # Check if review already exists
    existing_review = Review.objects.filter(
        reviewer=request.user,
        reviewee=application.worker,
        application=application
    ).exists()
    
    if existing_review:
        return JsonResponse({'success': False, 'error': 'Review already submitted'}, status=400)
    
    # Create review
    rating = int(request.POST.get('rating', 0))
    title = request.POST.get('title', '')
    comment = request.POST.get('comment', '')
    quality_rating = int(request.POST.get('quality_rating', 5))
    punctuality = int(request.POST.get('punctuality', 5))
    communication = int(request.POST.get('communication', 5))
    professionalism = int(request.POST.get('professionalism', 5))
    
    # Validate ratings
    if not (1 <= rating <= 5):
        return JsonResponse({'success': False, 'error': 'Invalid overall rating'}, status=400)
    
    if not all(1 <= r <= 5 for r in [quality_rating, punctuality, communication, professionalism]):
        return JsonResponse({'success': False, 'error': 'Invalid dimension ratings'}, status=400)
    
    if len(comment) < 20:
        return JsonResponse({'success': False, 'error': 'Review too short (min 20 characters)'}, status=400)
    
    # Create and save review
    review = Review.objects.create(
        reviewer=request.user,
        reviewee=application.worker,
        job=application.job,
        application=application,
        rating=rating,
        title=title,
        comment=comment,
        quality_rating=quality_rating,
        punctuality=punctuality,
        communication=communication,
        professionalism=professionalism,
        is_verified=True  # Verified because linked to completed application
    )
    
    # Update worker's average rating
    update_worker_rating(application.worker)
    
    return JsonResponse({
        'success': True,
        'message': 'Review submitted successfully!',
        'review_id': review.id
    })


def update_worker_rating(worker_user):
    """Update worker's overall rating based on all reviews"""
    try:
        worker_profile = worker_user.worker_profile
        reviews = Review.objects.filter(reviewee=worker_user).aggregate(
            avg_rating=Avg('rating'),
            count=Count('id')
        )
        
        if reviews['count'] > 0:
            worker_profile.rating = round(reviews['avg_rating'], 1)
            worker_profile.save()
    except:
        pass


@login_required
@require_http_methods(["POST"])
def reply_to_review(request, review_id):
    """Add a reply to a review"""
    review = get_object_or_404(Review, id=review_id)
    
    # Only the reviewer (original subject) can reply
    if request.user != review.reviewee:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    # Check if reply already exists
    if review.reply:
        return JsonResponse({'success': False, 'error': 'Reply already exists'}, status=400)
    
    message = request.POST.get('message', '').strip()
    if not message:
        return JsonResponse({'success': False, 'error': 'Reply message cannot be empty'}, status=400)
    
    if len(message) < 10:
        return JsonResponse({'success': False, 'error': 'Reply too short'}, status=400)
    
    # Create reply
    reply = ReviewReply.objects.create(
        review=review,
        author=request.user,
        message=message
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Reply posted successfully!',
        'reply_id': reply.id
    })


@login_required
def worker_reviews(request, worker_id):
    """Display all reviews for a worker"""
    worker_user = get_object_or_404(get_user_model(), id=worker_id, role='worker')
    reviews = Review.objects.filter(
        reviewee=worker_user
    ).select_related('reviewer').prefetch_related('reply').order_by('-created_at')
    
    # Calculate statistics
    stats = Review.objects.filter(reviewee=worker_user).aggregate(
        avg_rating=Avg('rating'),
        avg_quality=Avg('quality_rating'),
        avg_punctuality=Avg('punctuality'),
        avg_communication=Avg('communication'),
        avg_professionalism=Avg('professionalism'),
        count=Count('id')
    )
    
    # Rating distribution
    rating_dist = {}
    for i in range(1, 6):
        rating_dist[i] = Review.objects.filter(
            reviewee=worker_user, rating=i
        ).count()
    
    context = {
        'worker': worker_user,
        'reviews': reviews,
        'stats': stats,
        'rating_dist': rating_dist,
    }
    
    return render(request, 'reviews/worker_reviews.html', context)


# ═════════════════════════════════════════════════════════════════
# DISTANCE FILTERING VIEWS
# ═════════════════════════════════════════════════════════════════

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def filter_jobs_by_distance(user_lat, user_lon, radius_km, queryset=None):
    """Filter jobs within specified distance"""
    if queryset is None:
        queryset = Job.objects.filter(is_active=True)
    
    jobs_with_distance = []
    
    for job in queryset:
        if job.latitude and job.longitude:
            distance = haversine_distance(user_lat, user_lon, job.latitude, job.longitude)
            if distance <= radius_km:
                job.distance_km = round(distance, 1)
                jobs_with_distance.append(job)
        else:
            # Include jobs without location data
            job.distance_km = None
            jobs_with_distance.append(job)
    
    return jobs_with_distance


def filter_workers_by_distance(user_lat, user_lon, radius_km, queryset=None):
    """Filter workers within specified distance and working radius"""
    if queryset is None:
        queryset = WorkerProfile.objects.filter(user__is_active=True)
    
    workers_with_distance = []
    
    for worker in queryset:
        if worker.latitude and worker.longitude:
            distance = haversine_distance(user_lat, user_lon, worker.latitude, worker.longitude)
            
            # Check if within user's search radius AND within worker's working radius
            if distance <= radius_km and worker.is_within_radius(user_lat, user_lon):
                worker.distance_km = round(distance, 1)
                workers_with_distance.append(worker)
        else:
            # Include workers without location data
            worker.distance_km = None
            workers_with_distance.append(worker)
    
    return workers_with_distance


@login_required
def jobs_with_distance(request):
    """Browse jobs with distance filtering"""
    user = request.user
    
    # Get user's location
    user_lat = float(request.GET.get('lat')) if request.GET.get('lat') else None
    user_lon = float(request.GET.get('lon')) if request.GET.get('lon') else None
    radius_km = int(request.GET.get('radius', 10))
    
    # Start with all active jobs
    jobs_query = Job.objects.filter(is_active=True).select_related('employer')
    
    # Apply search filters
    search = request.GET.get('search')
    if search:
        jobs_query = jobs_query.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(skills_required__icontains=search)
        )
    
    category = request.GET.get('category')
    if category:
        jobs_query = jobs_query.filter(category=category)
    
    job_type = request.GET.get('job_type')
    if job_type:
        jobs_query = jobs_query.filter(job_type=job_type)
    
    # Apply distance filtering if user location is provided
    if user_lat and user_lon:
        jobs = filter_jobs_by_distance(user_lat, user_lon, radius_km, jobs_query)
        # Sort by distance
        jobs.sort(key=lambda x: x.distance_km if x.distance_km else float('inf'))
    else:
        jobs = list(jobs_query.order_by('-created_at'))
    
    context = {
        'jobs': jobs,
        'user_location': {'lat': user_lat, 'lon': user_lon} if user_lat and user_lon else None,
        'radius_km': radius_km,
        'search': search,
    }
    
    return render(request, 'jobs/list_with_distance.html', context)


@login_required
def workers_with_distance(request):
    """Browse workers with distance filtering"""
    user = request.user
    
    # Get user's location
    user_lat = float(request.GET.get('lat')) if request.GET.get('lat') else None
    user_lon = float(request.GET.get('lon')) if request.GET.get('lon') else None
    radius_km = int(request.GET.get('radius', 10))
    
    # Start with all active workers
    workers_query = WorkerProfile.objects.filter(user__is_active=True).select_related('user')
    
    # Apply search filters
    search = request.GET.get('search')
    if search:
        workers_query = workers_query.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(extra_skills__icontains=search)
        )
    
    skill = request.GET.get('skill')
    if skill:
        workers_query = workers_query.filter(
            Q(skills=skill) | Q(extra_skills__icontains=skill)
        )
    
    min_rating = request.GET.get('min_rating')
    if min_rating:
        workers_query = workers_query.filter(rating__gte=float(min_rating))
    
    # Apply distance filtering if user location is provided
    if user_lat and user_lon:
        workers = filter_workers_by_distance(user_lat, user_lon, radius_km, workers_query)
        # Sort by distance
        workers.sort(key=lambda x: x.distance_km if x.distance_km else float('inf'))
    else:
        workers = list(workers_query.order_by('-rating', '-total_jobs'))
    
    context = {
        'workers': workers,
        'user_location': {'lat': user_lat, 'lon': user_lon} if user_lat and user_lon else None,
        'radius_km': radius_km,
        'search': search,
    }
    
    return render(request, 'workers/list_with_distance.html', context)


@require_http_methods(["POST"])
def get_user_location(request):
    """AJAX endpoint to get user's location"""
    # This would typically receive latitude and longitude from client-side geolocation
    lat = request.POST.get('latitude')
    lon = request.POST.get('longitude')
    
    if lat and lon:
        return JsonResponse({
            'success': True,
            'latitude': float(lat),
            'longitude': float(lon)
        })
    
    return JsonResponse({'success': False, 'error': 'Unable to get location'}, status=400)


# ═════════════════════════════════════════════════════════════════
# HELPER FUNCTION TO ATTACH DISTANCE TO OBJECTS
# ═════════════════════════════════════════════════════════════════

def attach_distances_to_objects(objects, user_lat, user_lon, object_type='job'):
    """Generic function to attach distance data to objects"""
    if not user_lat or not user_lon:
        return objects
    
    for obj in objects:
        if object_type == 'job':
            if obj.latitude and obj.longitude:
                obj.distance_km = haversine_distance(user_lat, user_lon, obj.latitude, obj.longitude)
        elif object_type == 'worker':
            if obj.latitude and obj.longitude:
                obj.distance_km = haversine_distance(user_lat, user_lon, obj.latitude, obj.longitude)
    
    return objects
