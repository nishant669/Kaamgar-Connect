from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import CustomUser
from workers.models import WorkerProfile
from jobs.models import Job, JOB_CATEGORY_CHOICES
from applications.models import Application


# ---------------- LANDING ----------------
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    featured_jobs = Job.objects.filter(is_active=True)[:6]

    top_workers = CustomUser.objects.filter(
        role='worker',
        worker_profile__availability=True
    )[:4]

    return render(request, 'accounts/landing.html', {
        'categories': JOB_CATEGORY_CHOICES,
        'featured_jobs': featured_jobs,
        'top_workers': top_workers,
    })


# ---------------- REGISTER ----------------
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        otp = user.generate_otp()

        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            'noreply@kaamgar.com',
            [email],
            fail_silently=True
        )

        request.session['pending_user_id'] = user.id
        return redirect('accounts:verify_otp')

    return render(request, 'accounts/register.html')


# ---------------- OTP VERIFY ----------------
def verify_otp(request):
    user_id = request.session.get('pending_user_id')

    if not user_id:
        return redirect('accounts:register')

    user = CustomUser.objects.get(id=user_id)

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        if user.verify_otp(otp_input):
            login(request, user)
            del request.session['pending_user_id']
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid or expired OTP')

    return render(request, 'accounts/verify_otp.html')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            if not user.otp_verified:
                request.session['pending_user_id'] = user.id
                user.generate_otp()
                return redirect('accounts:verify_otp')

            login(request, user)
            return redirect('dashboard:home')

        messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')


# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# ---------------- PROFILE (🔥 IMPROVED) ----------------
@login_required
def profile_view(request):
    user = request.user

    worker_profile = None
    jobs_posted = None
    applications = None

    # Worker profile
    if user.role == 'worker':
        worker_profile, _ = WorkerProfile.objects.get_or_create(user=user)
        applications = Application.objects.filter(worker=user)

    # Employer data
    if user.role == 'employer':
        jobs_posted = Job.objects.filter(employer=user)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'worker_profile': worker_profile,
        'jobs_posted': jobs_posted,
        'applications': applications,
    })


# ---------------- CHANGE PASSWORD ----------------
@login_required
def change_password(request):
    if request.method == 'POST':
        new = request.POST.get('new_password')

        request.user.set_password(new)
        request.user.save()

        login(request, request.user)
        return redirect('accounts:profile')

    return render(request, 'accounts/change_password.html')


# ---------------- RESEND OTP ----------------
def resend_otp(request):
    user_id = request.session.get('pending_user_id')

    if not user_id:
        return redirect('accounts:register')

    user = CustomUser.objects.get(id=user_id)

    otp = user.generate_otp()

    send_mail(
        'Resend OTP',
        f'Your new OTP is {otp}',
        'noreply@kaamgar.com',
        [user.email],
        fail_silently=True
    )

    messages.success(request, 'OTP resent successfully')
    return redirect('accounts:verify_otp')