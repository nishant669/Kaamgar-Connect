from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, WorkerReview
from jobs.models import Job
from workers.models import WorkerProfile


@login_required
def apply(request, job_pk):

    job = get_object_or_404(
        Job,
        pk=job_pk,
        is_active=True
    )

    if request.user.role != 'worker':
        messages.error(
            request,
            'Only workers can apply.'
        )
        return redirect(
            'jobs:detail',
            pk=job_pk
        )

    if Application.objects.filter(
        job=job,
        worker=request.user
    ).exists():

        messages.warning(
            request,
            'You already applied to this job.'
        )

        return redirect(
            'jobs:detail',
            pk=job_pk
        )


    if request.method == 'POST':

        app = Application(
            job=job,
            worker=request.user,
            cover_note=request.POST.get(
                'cover_note',
                ''
            ).strip()
        )

        if request.FILES.get('resume'):
            app.resume = request.FILES['resume']

        app.save()

        try:
            from notifications.utils import notify_new_application

            notify_new_application(
                job.employer,
                request.user,
                job
            )

        except:
            pass

        messages.success(
            request,
            f'✅ Applied to "{job.title}" successfully!'
        )

        return render(
            request,
            'applications/apply.html',
            {'job': job}
        )

    return redirect(
        'jobs:detail',
        pk=job_pk
    )


@login_required
def withdraw(request, pk):

    app = get_object_or_404(
        Application,
        pk=pk,
        worker=request.user
    )

    if app.status == 'pending':

        app.delete()

        messages.success(
            request,
            'Application withdrawn.'
        )

    else:

        messages.error(
            request,
            'Cannot withdraw after it has been reviewed.'
        )

    return redirect(
        'applications:list'
    )


@login_required
def my_applications(request):

    apps = Application.objects.filter(
        worker=request.user
    ).select_related(
        'job',
        'job__employer'
    ).order_by('-applied_at')


    status_filter = request.GET.get('status','')

    if status_filter:
        apps = apps.filter(status=status_filter)


    all_apps = Application.objects.filter(
        worker=request.user
    )


    counts = {
        'all': all_apps.count(),
        'pending': all_apps.filter(status='pending').count(),
        'reviewed': all_apps.filter(status='reviewed').count(),
        'shortlisted': all_apps.filter(status='shortlisted').count(),
        'accepted': all_apps.filter(status='accepted').count(),
        'rejected': all_apps.filter(status='rejected').count(),
    }


    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': apps,
            'status_filter': status_filter,
            'counts': counts,
        }
    )


# -------------------------------
# REVIEW WORKER FEATURE
# -------------------------------

@login_required
def review_worker(request, job_id, worker_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    if request.user.role != "employer":
        messages.error(
            request,
            "Only employer can review worker"
        )
        return redirect(
            "jobs:detail",
            pk=job_id
        )


    if request.method == "POST":

        rating = request.POST.get("rating")
        review = request.POST.get("review")

        WorkerReview.objects.create(
            worker_id=worker_id,
            employer=request.user,
            job=job,
            rating=rating,
            review=review
        )

        # Update Worker Rating

        reviews = WorkerReview.objects.filter(
            worker_id=worker_id
        )

        avg_rating = sum(
            r.rating for r in reviews
        ) / reviews.count()

        WorkerProfile.objects.filter(
            user_id=worker_id
        ).update(
            rating=round(avg_rating, 1),
            total_jobs=reviews.count()
        )

        messages.success(
            request,
            "⭐ Review submitted successfully"
        )

        return redirect(
            "jobs:applicants",
            pk=job_id
        )