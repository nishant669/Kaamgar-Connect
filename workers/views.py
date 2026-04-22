from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from accounts.models import CustomUser
from workers.models import WorkerProfile, SKILL_CHOICES
from applications.models import WorkerReview 

def worker_list(request):
    workers = CustomUser.objects.filter(role='worker').select_related('worker_profile')
    skill     = request.GET.get('skills','')
    search    = request.GET.get('search','')
    available = request.GET.get('available','')
    min_rate  = request.GET.get('min_rate','')
    max_rate  = request.GET.get('max_rate','')
    min_exp   = request.GET.get('min_exp','')

    if skill:
        workers = workers.filter(worker_profile__skills=skill)
    if search:
        workers = workers.filter(
            Q(first_name__icontains=search)|Q(last_name__icontains=search)|
            Q(city__icontains=search)|Q(worker_profile__skills__icontains=search)|
            Q(worker_profile__extra_skills__icontains=search)
        )
    if available == '1':
        workers = workers.filter(worker_profile__availability=True)
    if min_rate:
        try: workers = workers.filter(worker_profile__daily_rate__gte=float(min_rate))
        except: pass
    if max_rate:
        try: workers = workers.filter(worker_profile__daily_rate__lte=float(max_rate))
        except: pass
    if min_exp:
        try: workers = workers.filter(worker_profile__experience_years__gte=int(min_exp))
        except: pass

    workers = workers.distinct().order_by('-worker_profile__aadhar_verified','-worker_profile__rating')
    return render(request,'workers/worker_list.html',{
        'workers': workers,
        'skill_choices': SKILL_CHOICES,
        'filters': {'skill':skill,'search':search,'available':available,
                    'min_rate':min_rate,'max_rate':max_rate,'min_exp':min_exp},
    })


def worker_detail(request, pk):

    profile_user = get_object_or_404(
        CustomUser,
        pk=pk,
        role='worker'
    )

    wp, _ = WorkerProfile.objects.get_or_create(
        user=profile_user
    )

    # Get Reviews
    reviews = WorkerReview.objects.filter(
        worker=profile_user
    ).select_related(
        "employer"
    ).order_by(
        "-created_at"
    )

    worker_details = [
        ('Primary Skill', wp.get_skills_display(), 'person-fill-gear'),
        ('Experience', f'{wp.experience_years} years', 'calendar3'),
        ('Daily Rate', f'₹{wp.daily_rate}/day', 'currency-rupee'),
        ('Jobs Done', str(wp.total_jobs), 'check2-circle'),
        ('Rating', f'{wp.rating}/5.0', 'star-fill'),
        ('Languages', wp.languages or 'Hindi, English', 'translate'),
        ('ID Verified', '✓ Verified' if wp.aadhar_verified else 'Pending', 'patch-check'),
        ('Availability', 'Available' if wp.availability else 'Unavailable','circle'),
    ]

    return render(
        request,
        'workers/worker_detail.html',
        {
            'profile_user': profile_user,
            'wp': wp,
            'reviews': reviews,
            'worker_details': worker_details,
        }
    )