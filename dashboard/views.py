from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from applications.models import Application
from jobs.models import Job, SavedJob
from workers.models import WorkerProfile
from accounts.models import CustomUser
from chat.models import Message, ChatRoom
from django.db.models import Q

@login_required
def home(request):
    user = request.user
    if user.role == 'worker':
        wp, _ = WorkerProfile.objects.get_or_create(user=user)
        all_apps = Application.objects.filter(worker=user).select_related('job','job__employer')
        saves    = SavedJob.objects.filter(user=user).count()
        rooms    = ChatRoom.objects.filter(worker=user)
        unread   = Message.objects.filter(room__in=rooms,is_read=False).exclude(sender=user).count()

        recommended = Job.objects.filter(
            is_active=True,category=wp.skills
        ).exclude(applications__worker=user).order_by('-is_featured','-created_at')[:6]
        if not recommended.exists():
            recommended = Job.objects.filter(is_active=True).exclude(
                applications__worker=user
            ).order_by('-is_featured','-created_at')[:6]

        checklist = [
            ('Full Name',    bool(user.first_name)),
            ('Phone Number', bool(user.phone)),
            ('Profile Photo',bool(user.profile_photo)),
            ('Bio',          bool(user.bio)),
            ('Daily Rate',   bool(wp.daily_rate)),
            ('Work Address', bool(wp.address)),
            ('Resume',       bool(wp.resume)),
            ('ID Verified',  bool(wp.aadhar_verified)),
            ('Extra Skills', bool(wp.extra_skills)),
            ('Experience',   bool(wp.experience_years)),
        ]
        completion = int(sum(v for _,v in checklist)/len(checklist)*100)

        stats = {
            'total_applications': all_apps.count(),
            'accepted':   all_apps.filter(status='accepted').count(),
            'pending':    all_apps.filter(status='pending').count(),
            'shortlisted':all_apps.filter(status='shortlisted').count(),
            'available_jobs': Job.objects.filter(is_active=True).count(),
            'saved_jobs': saves,
            'unread_messages': unread,
            'completion': completion,
        }
        return render(request,'dashboard/worker_dashboard.html',{
            'worker_profile': wp,
            'recent_applications': all_apps.order_by('-applied_at')[:6],
            'recommended_jobs': recommended,
            'stats': stats,
            'checklist': checklist,
            'completion': completion,
        })

    else:  # employer
        my_jobs  = Job.objects.filter(employer=user).order_by('-created_at')
        rooms    = ChatRoom.objects.filter(employer=user)
        unread   = Message.objects.filter(room__in=rooms,is_read=False).exclude(sender=user).count()
        total_apps  = Application.objects.filter(job__employer=user)
        top_workers = CustomUser.objects.filter(
            role='worker',worker_profile__availability=True
        ).select_related('worker_profile').order_by('-worker_profile__rating')[:5]
        recent_apps = Application.objects.filter(
            job__employer=user
        ).select_related('worker','worker__worker_profile','job').order_by('-applied_at')[:6]

        stats = {
            'active_jobs':      my_jobs.filter(is_active=True).count(),
            'total_applicants': total_apps.count(),
            'hired':            total_apps.filter(status='accepted').count(),
            'pending_apps':     total_apps.filter(status='pending').count(),
            'unread_messages':  unread,
            'total_jobs':       my_jobs.count(),
            'total_views':      sum(j.views for j in my_jobs),
        }
        return render(request,'dashboard/employer_dashboard.html',{
            'my_jobs': my_jobs.filter(is_active=True)[:5],
            'all_my_jobs_count': my_jobs.count(),
            'recent_applicants': recent_apps,
            'top_workers': top_workers,
            'stats': stats,
        })

@login_required
def analytics(request):
    if request.user.role != 'employer': return redirect('dashboard:home')
    user = request.user
    from django.db.models import Count
    from django.utils import timezone
    from datetime import timedelta
    jobs     = Job.objects.filter(employer=user)
    apps     = Application.objects.filter(job__employer=user)
    by_cat   = jobs.values('category').annotate(cnt=Count('id')).order_by('-cnt')
    by_status= apps.values('status').annotate(cnt=Count('id')).order_by('-cnt')
    # Last 6 months
    months = []
    for i in range(5,-1,-1):
        d = timezone.now() - timedelta(days=i*30)
        cnt = apps.filter(applied_at__month=d.month, applied_at__year=d.year).count()
        months.append({'label': d.strftime('%b'), 'count': cnt})
    return render(request,'dashboard/analytics.html',{
        'jobs': jobs, 'apps_by_status': by_status,
        'apps_by_cat': by_cat, 'monthly': months,
        'total_views': sum(j.views for j in jobs),
    })
