from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import CustomUser
from .email_utils import send_otp_email
from workers.models import WorkerProfile
from jobs.models import Job, JOB_CATEGORY_CHOICES
from applications.models import Application


# ───────────────── LANDING PAGE ─────────────────
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


# ───────────────── REGISTER ─────────────────
def register_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'worker')

        # Username check
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')

        # Email check
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')

        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'accounts/register.html')

        # Create inactive user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            is_active=False
        )

        # Generate OTP
        otp = user.generate_otp()

        # Send OTP email
        sent = send_otp_email(user, otp, purpose='register')

        if not sent:
            messages.warning(
                request,
                'OTP email could not be sent.'
            )

        # Save session
        request.session['pending_user_id'] = user.id

        return redirect('accounts:verify_otp')

    return render(request, 'accounts/register.html')


# ───────────────── VERIFY OTP ─────────────────
def verify_otp(request):

    user_id = request.session.get('pending_user_id')

    if not user_id:
        messages.error(request, 'Session expired.')
        return redirect('accounts:register')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':

        otp_input = request.POST.get('otp', '').strip()

        if user.verify_otp(otp_input):

            # Activate account
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=['is_active'])

            login(request, user)

            # SAFE delete
            request.session.pop('pending_user_id', None)

            messages.success(
                request,
                f'Welcome {user.username}! Email verified successfully.'
            )

            return redirect('dashboard:home')

        else:
            messages.error(
                request,
                'Invalid or expired OTP.'
            )

    return render(
        request,
        'accounts/verify_otp.html',
        {
            'user_email': user.email
        }
    )


# ───────────────── RESEND OTP ─────────────────
def resend_otp(request):

    user_id = request.session.get('pending_user_id')

    if not user_id:
        return redirect('accounts:register')

    user = get_object_or_404(CustomUser, id=user_id)

    otp = user.generate_otp()

    sent = send_otp_email(user, otp, purpose='resend')

    if sent:
        messages.success(request, 'New OTP sent successfully.')
    else:
        messages.error(request, 'Unable to send OTP.')

    return redirect('accounts:verify_otp')


# ───────────────── LOGIN ─────────────────
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            # OTP not verified
            if not user.otp_verified:

                otp = user.generate_otp()

                send_otp_email(user, otp, purpose='login')

                request.session['pending_user_id'] = user.id

                return redirect('accounts:verify_otp')

            # Normal login
            login(request, user)

            return redirect('dashboard:home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# ───────────────── LOGOUT ─────────────────
def logout_view(request):

    logout(request)

    return redirect('accounts:login')


# ───────────────── PROFILE ─────────────────
@login_required
def profile_view(request):

    user = request.user

    worker_profile = None
    jobs_posted = None
    applications = None

    if user.role == 'worker':

        worker_profile, _ = WorkerProfile.objects.get_or_create(user=user)

        applications = Application.objects.filter(worker=user)

    elif user.role == 'employer':

        jobs_posted = Job.objects.filter(employer=user)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'worker_profile': worker_profile,
        'jobs_posted': jobs_posted,
        'applications': applications,
    })


# ───────────────── CHANGE PASSWORD ─────────────────
@login_required
def change_password(request):

    if request.method == 'POST':

        new_password = request.POST.get('new_password', '')

        request.user.set_password(new_password)

        request.user.save()

        login(request, request.user)

        messages.success(request, 'Password changed successfully.')

        return redirect('accounts:profile')

    return render(request, 'accounts/change_password.html')