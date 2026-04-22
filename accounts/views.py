from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from workers.models import WorkerProfile
from jobs.models import Job, JOB_CATEGORY_CHOICES

DEVELOPERS = [
    {'name':'Nishant Chourasiya','role':'Lead Developer & Architect','bio':'Full-stack developer passionate about building scalable solutions for India\'s blue-collar workforce.','skills':['Django','React','MySQL','TailwindCSS'],'email':'nishant@kaamgar.com'},
    {'name':'Priya Sharma','role':'UI/UX Designer','bio':'Creative designer focused on making technology accessible and beautiful for everyone.','skills':['Figma','Adobe XD','User Research','Bootstrap'],'email':'priya@kaamgar.com'},
    {'name':'Rahul Verma','role':'Backend Engineer','bio':'Specialist in distributed systems and database optimization for high-traffic platforms.','skills':['Python','MySQL','Docker','REST APIs'],'email':'rahul@kaamgar.com'},
]
FEATURES = [
    {'icon':'📍','title':'Hyper-Local Talent','desc':'Find verified workers within 5km of your location in Bhopal & Indore. Same-day availability guaranteed.'},
    {'icon':'🛡️','title':'Aadhaar Verified','desc':'All workers pass OTP verification and government ID checks for maximum safety and trust.'},
    {'icon':'⚡','title':'Instant Connection','desc':'Built-in chat and messaging — connect with workers or employers in seconds, not days.'},
    {'icon':'🏆','title':'Rating & Reviews','desc':'Transparent ratings and verified reviews help you make confident, informed hiring decisions.'},
    {'icon':'🌐','title':'Hindi & English','desc':'Fully bilingual platform — use Kaamgar Connect comfortably in your preferred language.'},
    {'icon':'📊','title':'Smart Dashboard','desc':'Role-based dashboards with real-time analytics, application tracking, and AI talent matching.'},
]
STEPS = [
    {'title':'Create Account','desc':'Register as Worker or Employer. Verify your identity with OTP and Government ID for full access.'},
    {'title':'Post or Apply','desc':'Employers post jobs with full details. Workers browse, filter, and apply with a single click.'},
    {'title':'Connect & Work','desc':'Chat directly, finalize the deal, and get work done. Rate each other after completion.'},
]
TESTIMONIALS = [
    {'quote':'Found a skilled electrician within 2 hours! The worker was verified and incredibly professional. Highly recommended.','name':'Ramesh Gupta','role':'Employer','city':'Bhopal','color':'linear-gradient(135deg,#0d6efd,#6366f1)'},
    {'quote':'I got 5 job offers in my first week! Kaamgar Connect made it so easy to showcase my skills to employers.','name':'Suresh Kumar','role':'Electrician','city':'Indore','color':'linear-gradient(135deg,#7c3aed,#a855f7)'},
    {'quote':'The chat feature is excellent. Direct negotiation with workers made the whole hiring process smooth and transparent.','name':'Priya Sharma','role':'Employer','city':'Bhopal','color':'linear-gradient(135deg,#ea580c,#fb923c)'},
]
CONTACT_INFO = [
    {'icon':'📧','label':'Email Us','value':'hello@kaamgar.com'},
    {'icon':'📱','label':'Call Us','value':'+91 98765 43210'},
    {'icon':'📍','label':'Office','value':'Bhopal, Madhya Pradesh 462001'},
    {'icon':'⏰','label':'Hours','value':'Mon–Sat, 9am – 6pm IST'},
]

def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    featured_jobs = Job.objects.filter(is_active=True).select_related('employer').order_by('-created_at')[:6]
    top_workers   = CustomUser.objects.filter(
        role='worker', worker_profile__availability=True
    ).select_related('worker_profile').order_by('-worker_profile__rating')[:4]
    return render(request, 'accounts/landing.html', {
        'categories':   JOB_CATEGORY_CHOICES,
        'developers':   DEVELOPERS,
        'features':     FEATURES,
        'steps':        STEPS,
        'testimonials': TESTIMONIALS,
        'contact_info': CONTACT_INFO,
        'featured_jobs': featured_jobs,
        'top_workers':   top_workers,
    })

def register_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username','').strip()
        email     = request.POST.get('email','').strip()
        password  = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        role      = request.POST.get('role','worker')
        full_name = request.POST.get('full_name','').strip()
        phone     = request.POST.get('phone','').strip()
        city      = request.POST.get('city','').strip()

        if password != password2:
            messages.error(request,'Passwords do not match.'); return render(request,'accounts/register.html')
        if len(password) < 8:
            messages.error(request,'Password must be at least 8 characters.'); return render(request,'accounts/register.html')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request,'Username already taken.'); return render(request,'accounts/register.html')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request,'Email already registered.'); return render(request,'accounts/register.html')

        user = CustomUser.objects.create_user(username=username,email=email,password=password,role=role,phone=phone,city=city)
        names = full_name.split(' ',1)
        user.first_name = names[0]
        user.last_name  = names[1] if len(names)>1 else ''
        otp = user.generate_otp(); user.save()
        send_mail('Kaamgar Connect – Verify Your Email',f'Hello {user.first_name},\n\nYour OTP is: {otp}\nValid for 10 minutes.','noreply@kaamgar.com',[email],fail_silently=True)
        # Create employer profile if needed
        if role == 'employer':
            try:
                from employers.models import Employer
                Employer.objects.get_or_create(user=user)
            except: pass
        request.session['pending_user_id'] = user.id
        messages.info(request,f'OTP sent to {email}. (Dev OTP: {otp})')
        return redirect('accounts:verify_otp')
    return render(request,'accounts/register.html')

def verify_otp(request):
    user_id = request.session.get('pending_user_id')
    if not user_id: return redirect('accounts:register')
    # Get user email for display in template
    email = ''
    try:
        _u = CustomUser.objects.get(id=user_id)
        email = _u.email
    except CustomUser.DoesNotExist:
        pass
    if request.method == 'POST':
        otp_input = request.POST.get('otp','').strip()
        try:
            user = CustomUser.objects.get(id=user_id)
            if user.otp == otp_input:
                user.otp_verified=True; user.otp=''; user.save()
                if user.role == 'worker': WorkerProfile.objects.get_or_create(user=user)
                login(request,user)
                del request.session['pending_user_id']
                messages.success(request,f'Welcome to Kaamgar Connect, {user.first_name or user.username}! 🎉')
                return redirect('dashboard:home')
            else:
                messages.error(request,'Invalid OTP. Please try again.')
        except CustomUser.DoesNotExist:
            messages.error(request,'Session expired. Please register again.')
            return redirect('accounts:register')
    return render(request,'accounts/verify_otp.html', {'email': email})

def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request,username=username,password=password)
        if user:
            if not user.otp_verified:
                request.session['pending_user_id']=user.id
                otp=user.generate_otp()
                send_mail('Kaamgar Connect – OTP',f'Your OTP: {otp}','noreply@kaamgar.com',[user.email],fail_silently=True)
                messages.info(request,f'Please verify email first. (Dev OTP: {otp})')
                return redirect('accounts:verify_otp')
            login(request,user)
            messages.success(request,f'Welcome back, {user.first_name or user.username}! 👋')
            return redirect(request.GET.get('next','dashboard:home'))
        else: messages.error(request,'Invalid username or password.')
    return render(request,'accounts/login.html')

def logout_view(request):
    logout(request); messages.success(request,'Logged out successfully. See you soon!')
    return redirect('accounts:landing')

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name',user.first_name).strip()
        user.last_name  = request.POST.get('last_name',user.last_name).strip()
        user.phone      = request.POST.get('phone',user.phone).strip()
        user.city       = request.POST.get('city',user.city).strip()
        user.bio        = request.POST.get('bio',user.bio).strip()
        user.language   = request.POST.get('language',user.language)
        if request.FILES.get('profile_photo'): user.profile_photo = request.FILES['profile_photo']
        user.save()
        if user.role == 'worker':
            wp,_ = WorkerProfile.objects.get_or_create(user=user)
            wp.skills           = request.POST.get('skills',wp.skills)
            wp.experience_years = int(request.POST.get('experience_years',0) or 0)
            wp.daily_rate       = float(request.POST.get('daily_rate',0) or 0)
            wp.availability     = request.POST.get('availability')=='on'
            wp.address          = request.POST.get('address',wp.address).strip()
            wp.extra_skills     = request.POST.get('extra_skills',wp.extra_skills).strip()
            wp.portfolio_url    = request.POST.get('portfolio_url',wp.portfolio_url).strip()
            wp.languages        = request.POST.get('languages',wp.languages).strip()
            if request.FILES.get('resume'):
                wp.resume = request.FILES['resume']
            wp.save()
        elif user.role == 'employer':
            try:
                from employers.models import Employer
                ep,_ = Employer.objects.get_or_create(user=user)
                ep.company_name = request.POST.get('company_name',ep.company_name).strip()
                ep.industry     = request.POST.get('industry',ep.industry).strip()
                ep.company_size = request.POST.get('company_size',ep.company_size)
                ep.description  = request.POST.get('company_desc',ep.description).strip()
                ep.website      = request.POST.get('website',ep.website).strip()
                if request.FILES.get('company_logo'): ep.company_logo = request.FILES['company_logo']
                ep.save()
            except: pass
        messages.success(request,'Profile updated successfully! ✅')
        return redirect('accounts:profile')
    worker_profile=None; employer_profile=None
    if user.role=='worker': worker_profile,_=WorkerProfile.objects.get_or_create(user=user)
    elif user.role=='employer':
        try:
            from employers.models import Employer
            employer_profile,_=Employer.objects.get_or_create(user=user)
        except: pass
    # Build account details list
    account_details = [
        ('Username',     user.username,                          'text-muted'),
        ('Account Type', user.role.capitalize(),                 'badge-primary kc-badge'),
        ('Member Since', user.created_at.strftime('%b %Y'),     'text-muted'),
        ('Email',        '✓ Verified' if user.otp_verified else '⚠ Unverified',
         'text-success fw-600' if user.otp_verified else 'text-danger fw-600'),
        ('Last Login',   user.last_login.strftime('%b %d, %Y') if user.last_login else 'Never', 'text-muted'),
    ]
    checklist = []
    if user.role == 'worker' and worker_profile:
        checklist = [
            ('Full Name',     bool(user.first_name)),
            ('Phone Number',  bool(user.phone)),
            ('Profile Photo', bool(user.profile_photo)),
            ('Bio',           bool(user.bio)),
            ('Daily Rate',    bool(worker_profile.daily_rate)),
            ('Experience',    bool(worker_profile.experience_years)),
            ('Work Address',  bool(worker_profile.address)),
            ('Resume',        bool(worker_profile.resume)),
            ('ID Verified',   bool(worker_profile.aadhar_verified)),
            ('Extra Skills',  bool(worker_profile.extra_skills)),
        ]
    return render(request,'accounts/profile.html',{
        'worker_profile':worker_profile,
        'employer_profile':employer_profile,
        'account_details': account_details,
        'checklist': checklist,
    })

@login_required
def change_password(request):
    if request.method=='POST':
        old=request.POST.get('old_password','')
        new=request.POST.get('new_password','')
        confirm=request.POST.get('confirm_password','')
        if not request.user.check_password(old): messages.error(request,'Current password is incorrect.')
        elif new!=confirm: messages.error(request,'New passwords do not match.')
        elif len(new)<8: messages.error(request,'Password must be at least 8 characters.')
        else:
            request.user.set_password(new); request.user.save()
            login(request,request.user)
            messages.success(request,'Password changed successfully! 🔐')
        return redirect('accounts:profile')
    return render(request,'accounts/change_password.html')
