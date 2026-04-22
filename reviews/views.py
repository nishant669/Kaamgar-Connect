from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from accounts.models import CustomUser
from workers.models import WorkerProfile

@login_required
def leave_review(request, user_pk):
    if request.method != 'POST':
        return redirect('workers:detail', pk=user_pk)
    reviewee = get_object_or_404(CustomUser, pk=user_pk)
    if reviewee == request.user:
        messages.error(request, "You cannot review yourself.")
        return redirect('workers:detail', pk=user_pk)
    rating  = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '').strip()
    job_id  = request.POST.get('job_id')
    job     = None
    if job_id:
        from jobs.models import Job
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            pass
    Review.objects.update_or_create(
        reviewer=request.user, reviewee=reviewee, job=job,
        defaults={'rating': rating, 'comment': comment}
    )
    # Update worker average rating
    if reviewee.role == 'worker':
        wp, _ = WorkerProfile.objects.get_or_create(user=reviewee)
        reviews = Review.objects.filter(reviewee=reviewee)
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / reviews.count()
            wp.rating = round(avg, 1)
            wp.save()
    messages.success(request, f'Review submitted for {reviewee.get_full_name() or reviewee.username}!')
    return redirect('workers:detail', pk=user_pk)
