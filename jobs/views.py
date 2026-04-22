from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Job, SavedJob, JOB_CATEGORY_CHOICES, JOB_TYPE_CHOICES, EXPERIENCE_CHOICES
from applications.models import Application
import datetime

def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related('employer')
    category   = request.GET.get('category','')
    location   = request.GET.get('location','')
    job_type   = request.GET.get('job_type','')
    experience = request.GET.get('experience','')
    salary_min = request.GET.get('salary_min','')
    search     = request.GET.get('search','')

    if category:   jobs = jobs.filter(category=category)
    if location:   jobs = jobs.filter(location__icontains=location)
    if job_type:   jobs = jobs.filter(job_type=job_type)
    if experience: jobs = jobs.filter(experience_req=experience)
    if salary_min:
        try: jobs = jobs.filter(salary_min__gte=float(salary_min))
        except: pass
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)|Q(description__icontains=search)|
            Q(skills_required__icontains=search)|Q(location__icontains=search)
        )

    saved_ids = set()
    if request.user.is_authenticated:
        saved_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    jobs = jobs.distinct().order_by('-is_featured','-created_at')
    paginator = Paginator(jobs, 12)
    page_obj  = paginator.get_page(request.GET.get('page',1))

    return render(request,'jobs/job_list.html',{
        'jobs': page_obj, 'page_obj': page_obj,
        'category': category, 'location': location, 'job_type': job_type,
        'experience': experience, 'salary_min': salary_min, 'search': search,
        'saved_ids': saved_ids,
        'categories':   JOB_CATEGORY_CHOICES,
        'job_types':    JOB_TYPE_CHOICES,
        'exp_choices':  EXPERIENCE_CHOICES,
    })

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    # Track view
    Job.objects.filter(pk=pk).update(views=job.views+1)

    already_applied = False
    is_saved = False
    if request.user.is_authenticated and request.user.role == 'worker':
        already_applied = Application.objects.filter(job=job, worker=request.user).exists()
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()

    related_jobs = Job.objects.filter(
        category=job.category, is_active=True
    ).exclude(pk=pk)[:4]

    job_details = [
        ('currency-rupee', 'Salary', f'₹{job.salary_min:,.0f}–{job.salary_max:,.0f}/mo'),
        ('geo-alt', 'Location', job.location),
        ('clock', 'Job Type', job.get_job_type_display()),
        ('calendar', 'Posted', job.created_at.strftime('%b %d, %Y')),
    ]
    if job.deadline:
        job_details.append(('calendar-x', 'Deadline', job.deadline.strftime('%b %d, %Y')))
    return render(request,'jobs/job_detail.html',{
        'job': job, 'already_applied': already_applied,
        'is_saved': is_saved, 'related_jobs': related_jobs,
    })

@login_required
def toggle_save_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    if not created:
        saved.delete()
        msg = 'Job removed from saved jobs.'
        is_saved = False
    else:
        msg = 'Job saved successfully!'
        is_saved = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': is_saved, 'msg': msg})
    messages.success(request, msg)
    return redirect('jobs:detail', pk=pk)

@login_required
def saved_jobs(request):
    saves = SavedJob.objects.filter(user=request.user).select_related('job','job__employer').order_by('-saved_at')
    return render(request,'jobs/saved_jobs.html',{'saves': saves})

@login_required
def post_job(request):
    if request.user.role != 'employer':
        messages.error(request,'Only employers can post jobs.'); return redirect('dashboard:home')
    if request.method == 'POST':
        import datetime
        deadline_str = request.POST.get('deadline','')
        deadline = None
        if deadline_str:
            try: deadline = datetime.date.fromisoformat(deadline_str)
            except: pass
        job = Job.objects.create(
            employer=request.user,
            title=request.POST['title'],
            title_hi=request.POST.get('title_hi',''),
            category=request.POST['category'],
            job_type=request.POST.get('job_type','full_time'),
            experience_req=request.POST.get('experience_req','fresher'),
            skills_required=request.POST.get('skills_required',''),
            description=request.POST['description'],
            description_hi=request.POST.get('description_hi',''),
            location=request.POST['location'],
            salary_min=float(request.POST.get('salary_min',0) or 0),
            salary_max=float(request.POST.get('salary_max',0) or 0),
            openings=int(request.POST.get('openings',1) or 1),
            deadline=deadline,
        )
        # Fire notification to matching workers
        try:
            from notifications.utils import notify
            from accounts.models import CustomUser
            from workers.models import WorkerProfile
            matching = CustomUser.objects.filter(
                role='worker', worker_profile__skills=job.category
            )
            for w in matching[:50]:
                notify(w,'job',f'New {job.get_category_display()} job: {job.title}',
                       f'Salary: ₹{job.salary_min:,.0f}–{job.salary_max:,.0f}/mo · {job.location}',
                       f'/jobs/{job.pk}/')
        except: pass
        messages.success(request, f'Job "{job.title}" posted successfully! 🎉')
        return redirect('jobs:my_jobs')
    return render(request,'jobs/post_job.html',{
        'categories': JOB_CATEGORY_CHOICES,
        'job_types':  JOB_TYPE_CHOICES,
        'exp_choices':EXPERIENCE_CHOICES,
    })

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        import datetime
        deadline_str = request.POST.get('deadline','')
        deadline = None
        if deadline_str:
            try: deadline = datetime.date.fromisoformat(deadline_str)
            except: pass
        for field in ['title','title_hi','category','job_type','experience_req',
                      'skills_required','description','description_hi','location']:
            setattr(job, field, request.POST.get(field, getattr(job, field)))
        job.salary_min = float(request.POST.get('salary_min',0) or 0)
        job.salary_max = float(request.POST.get('salary_max',0) or 0)
        job.openings   = int(request.POST.get('openings',1) or 1)
        job.deadline   = deadline
        job.save()
        messages.success(request,'Job updated successfully!')
        return redirect('jobs:my_jobs')
    return render(request,'jobs/post_job.html',{
        'job':job,'editing':True,
        'categories':JOB_CATEGORY_CHOICES,'job_types':JOB_TYPE_CHOICES,'exp_choices':EXPERIENCE_CHOICES,
    })

@login_required
def my_jobs(request):
    if request.user.role != 'employer': return redirect('dashboard:home')
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    active_count = jobs.filter(is_active=True).count()
    total_apps   = sum(j.applications.count() for j in jobs)
    total_views  = sum(j.views for j in jobs)
    return render(request,'jobs/my_jobs.html',{
        'jobs':jobs,'active_count':active_count,
        'total_apps':total_apps,'total_views':total_views,
    })

@login_required
def job_applicants(request, pk):
    job  = get_object_or_404(Job, pk=pk, employer=request.user)
    apps = Application.objects.filter(job=job).select_related('worker','worker__worker_profile')
    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        status = request.POST.get('status')
        if status in ['pending','reviewed','shortlisted','accepted','rejected']:
            app = Application.objects.filter(id=app_id, job=job).first()
            if app:
                app.status = status
                app.save()
                try:
                    from notifications.utils import notify_status_change
                    notify_status_change(app.worker, job, status)
                except: pass
            messages.success(request,'Application status updated.')
        return redirect('jobs:applicants', pk=pk)
    status_filter = request.GET.get('status','')
    if status_filter: apps = apps.filter(status=status_filter)
    from applications.models import Application as App
    counts = {s: App.objects.filter(job=job, status=s).count()
              for s in ['pending','reviewed','shortlisted','accepted','rejected']}
    counts['all'] = App.objects.filter(job=job).count()
    return render(request,'jobs/applicants.html',{
        'job':job,'applications':apps,
        'status_filter':status_filter,'counts':counts,
    })

@login_required
def toggle_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    job.is_active = not job.is_active; job.save()
    messages.success(request, f'Job "{"activated" if job.is_active else "paused"}".')
    return redirect('jobs:my_jobs')

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        title = job.title; job.delete()
        messages.success(request, f'Job "{title}" deleted.')
    return redirect('jobs:my_jobs')
