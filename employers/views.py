from django.shortcuts import render, get_object_or_404
from .models import Employer

def employer_list(request):
    employers = Employer.objects.select_related('user').all()
    return render(request, 'employers/list.html', {'employers': employers})

def employer_detail(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    jobs = employer.user.posted_jobs.filter(is_active=True)
    return render(request, 'employers/detail.html', {'employer': employer, 'jobs': jobs})
