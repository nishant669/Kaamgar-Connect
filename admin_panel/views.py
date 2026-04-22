from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from accounts.models import CustomUser
from jobs.models import Job
from applications.models import Application
from workers.models import WorkerProfile
from employers.models import Employer

@staff_member_required
def admin_dashboard(request):
    now = timezone.now()
    month_ago = now - timedelta(days=30)
    week_ago  = now - timedelta(days=7)

    stats = {
        'total_users':    CustomUser.objects.count(),
        'total_workers':  CustomUser.objects.filter(role='worker').count(),
        'total_employers':CustomUser.objects.filter(role='employer').count(),
        'total_jobs':     Job.objects.count(),
        'active_jobs':    Job.objects.filter(is_active=True).count(),
        'total_apps':     Application.objects.count(),
        'new_users_week': CustomUser.objects.filter(created_at__gte=week_ago).count(),
        'new_jobs_month': Job.objects.filter(created_at__gte=month_ago).count(),
        'pending_apps':   Application.objects.filter(status='pending').count(),
        'accepted_apps':  Application.objects.filter(status='accepted').count(),
        'verified_workers': WorkerProfile.objects.filter(aadhar_verified=True).count(),
    }
    recent_users = CustomUser.objects.order_by('-date_joined')[:10]
    recent_jobs  = Job.objects.select_related('employer').order_by('-created_at')[:10]
    pending_verifications = WorkerProfile.objects.filter(aadhar_verified=False).select_related('user')[:10]

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_jobs': recent_jobs,
        'pending_verifications': pending_verifications,
    })

@staff_member_required
def verify_worker(request, user_pk):
    wp = get_object_or_404(WorkerProfile, user__pk=user_pk)
    wp.aadhar_verified = True
    wp.save()
    messages.success(request, f'{wp.user.get_full_name()} verified successfully!')
    return redirect('admin_panel:dashboard')

@staff_member_required
def manage_users(request):
    role   = request.GET.get('role', '')
    search = request.GET.get('search', '')
    users  = CustomUser.objects.order_by('-date_joined')
    if role:   users = users.filter(role=role)
    if search: users = users.filter(Q(username__icontains=search)|Q(email__icontains=search)|Q(first_name__icontains=search))
    return render(request, 'admin_panel/users.html', {'users': users, 'role': role, 'search': search})

@staff_member_required
def toggle_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'User {"activated" if user.is_active else "deactivated"}.')
    return redirect('admin_panel:users')

@staff_member_required
def manage_jobs(request):
    jobs = Job.objects.select_related('employer').order_by('-created_at')
    return render(request, 'admin_panel/jobs.html', {'jobs': jobs})

@staff_member_required
def toggle_job_featured(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.is_featured = not job.is_featured
    job.save()
    messages.success(request, f'Job {"featured" if job.is_featured else "unfeatured"}.')
    return redirect('admin_panel:jobs')
