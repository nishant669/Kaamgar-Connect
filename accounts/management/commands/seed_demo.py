"""
python manage.py seed_demo
Seeds complete demo data for Kaamgar Connect.
All demo accounts use password: Demo@1234
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from workers.models import WorkerProfile
from employers.models import Employer
from jobs.models import Job, SavedJob
from applications.models import Application
from notifications.models import Notification
from reviews.models import Review

User = get_user_model()

WORKERS = [
    {'username':'rahul_e',   'first':'Rahul',   'last':'Sharma',   'email':'rahul@demo.com',   'city':'Bhopal',  'phone':'+919876543210', 'skill':'electrician', 'exp':5, 'rate':800,  'rating':4.8,'total':15,'bio':'Experienced electrician specializing in industrial and residential wiring.'},
    {'username':'suresh_p',  'first':'Suresh',  'last':'Kumar',    'email':'suresh@demo.com',  'city':'Indore',  'phone':'+919876543211', 'skill':'plumber',     'exp':8, 'rate':700,  'rating':4.5,'total':22,'bio':'Expert plumber with 8 years in residential and commercial projects.'},
    {'username':'amit_c',    'first':'Amit',    'last':'Patel',    'email':'amit@demo.com',    'city':'Bhopal',  'phone':'+919876543212', 'skill':'carpenter',   'exp':3, 'rate':600,  'rating':4.2,'total':8, 'bio':'Skilled carpenter for furniture, interiors, and custom woodwork.'},
    {'username':'priya_cook','first':'Priya',   'last':'Devi',     'email':'priya@demo.com',   'city':'Bhopal',  'phone':'+919876543213', 'skill':'cook',        'exp':6, 'rate':500,  'rating':4.9,'total':30,'bio':'Professional chef experienced in North Indian, South Indian, and Chinese cuisines.'},
    {'username':'vikram_s',  'first':'Vikram',  'last':'Singh',    'email':'vikram@demo.com',  'city':'Indore',  'phone':'+919876543214', 'skill':'security',    'exp':4, 'rate':550,  'rating':4.3,'total':12,'bio':'Certified security professional with experience in corporate and event security.'},
    {'username':'anita_m',   'first':'Anita',   'last':'Sharma',   'email':'anita@demo.com',   'city':'Bhopal',  'phone':'+919876543215', 'skill':'mason',       'exp':10,'rate':750,  'rating':4.7,'total':28,'bio':'Senior mason with expertise in brick laying, plastering, and RCC work.'},
    {'username':'mohan_d',   'first':'Mohan',   'last':'Verma',    'email':'mohan@demo.com',   'city':'Indore',  'phone':'+919876543216', 'skill':'driver',      'exp':7, 'rate':600,  'rating':4.6,'total':20,'bio':'Professional driver with LMV and HMV licenses. Clean record, punctual.'},
    {'username':'ravi_ac',   'first':'Ravi',    'last':'Gupta',    'email':'ravi@demo.com',    'city':'Bhopal',  'phone':'+919876543217', 'skill':'ac_technician','exp':4,'rate':900,  'rating':4.4,'total':18,'bio':'AC technician for split, window, and cassette ACs. Quick diagnosis and repair.'},
]

EMPLOYERS = [
    {'username':'buildright', 'first':'BuildRight',  'last':'Infra',     'email':'build@demo.com',   'city':'Bhopal',  'company':'BuildRight Infrastructure Pvt. Ltd.', 'industry':'Construction'},
    {'username':'techcorp',   'first':'TechCorp',    'last':'Solutions',  'email':'tech@demo.com',   'city':'Indore',  'company':'TechCorp Solutions Ltd.',              'industry':'Technology'},
    {'username':'homefix',    'first':'HomeFix',     'last':'Services',   'email':'homefix@demo.com','city':'Bhopal',  'company':'HomeFix Home Services',                'industry':'Home Services'},
    {'username':'securepro',  'first':'SecurePro',   'last':'Agency',     'email':'secure@demo.com', 'city':'Indore',  'company':'SecurePro Security Agency',            'industry':'Security'},
]

JOBS = [
    {'title':'Senior Electrician Required',        'employer_idx':0,'cat':'electrical','loc':'Bhopal, MP',  'smin':20000,'smax':30000,'exp':'3_5','skills':'Wiring, Panel Board, Safety, Industrial','desc':'We need an experienced electrician for commercial building wiring and maintenance work. 5+ years required.\n\nResponsibilities:\n- Industrial and commercial electrical installations\n- Panel board maintenance\n- Safety compliance\n\nBenefits: ESI, PF, Bonus'},
    {'title':'Plumber – Residential Project',       'employer_idx':2,'cat':'plumbing',  'loc':'Indore, MP',  'smin':15000,'smax':22000,'exp':'1_2','skills':'Pipe Fitting, Plumbing, Sanitation','desc':'Looking for a skilled plumber for residential plumbing installation and repairs in new housing society.'},
    {'title':'Security Guard – Night Shift',        'employer_idx':3,'cat':'security',  'loc':'Bhopal, MP',  'smin':12000,'smax':15000,'exp':'1_2','skills':'Security, Patrol, CCTV, Communication','desc':'Security guard for industrial premises. Night shift 10PM–6AM. Valid police verification required.'},
    {'title':'Cook for Corporate Canteen',          'employer_idx':2,'cat':'cooking',   'loc':'Bhopal, MP',  'smin':18000,'smax':25000,'exp':'3_5','skills':'North Indian, South Indian, Canteen Management','desc':'Experienced cook for corporate canteen serving 100+ employees. Must know multi-cuisine cooking.','featured':True},
    {'title':'Carpenter – Interior Work',           'employer_idx':0,'cat':'carpentry', 'loc':'Indore, MP',  'smin':16000,'smax':24000,'exp':'1_2','skills':'Furniture, Interior, Wood Work, POP','desc':'Skilled carpenter for custom furniture and interior woodwork in luxury villas project.'},
    {'title':'Mason – Construction Site',           'employer_idx':0,'cat':'construction','loc':'Bhopal, MP','smin':14000,'smax':20000,'exp':'fresher','skills':'Brick Laying, Plastering, Concrete','desc':'Experienced mason for residential construction. RCC, brick masonry, and plastering work.'},
    {'title':'Driver – Corporate Fleet',            'employer_idx':1,'cat':'driving',   'loc':'Indore, MP',  'smin':15000,'smax':20000,'exp':'3_5','skills':'LMV, HMV, Navigation, Traffic Rules','desc':'Professional driver for corporate cab service. AC car provided. 8AM–8PM shift.','featured':True},
    {'title':'AC Technician – Service Center',      'employer_idx':2,'cat':'ac_tech',   'loc':'Bhopal, MP',  'smin':18000,'smax':28000,'exp':'1_2','skills':'Split AC, Window AC, Gas Refilling, PCB','desc':'AC technician for installation, servicing, and repair. ITI/Diploma in Electrical preferred.'},
    {'title':'Painter – Commercial Building',       'employer_idx':0,'cat':'painting',  'loc':'Bhopal, MP',  'smin':12000,'smax':18000,'exp':'fresher','skills':'Wall Painting, Texture, Putty, Polish','desc':'Painter required for large commercial building exterior and interior painting. Material provided.'},
    {'title':'Welder – Fabrication Shop',           'employer_idx':1,'cat':'welding',   'loc':'Indore, MP',  'smin':16000,'smax':22000,'exp':'1_2','skills':'MIG Welding, TIG Welding, Fabrication, Metal','desc':'Skilled welder for steel fabrication workshop. Arc, MIG, TIG welding experience required.'},
    {'title':'Office Cleaning Staff',               'employer_idx':1,'cat':'cleaning',  'loc':'Indore, MP',  'smin':8000, 'smax':12000,'exp':'fresher','skills':'Cleaning, Housekeeping, Sanitization','desc':'Cleaning staff for corporate office. Morning shift 7AM–3PM. Cleaning supplies provided.'},
    {'title':'Electrician – Solar Panel Installation','employer_idx':1,'cat':'electrical','loc':'Bhopal, MP','smin':22000,'smax':35000,'exp':'3_5','skills':'Solar, Inverter, Panel, Electrical','desc':'Electrician with solar experience for rooftop solar installation projects across MP.'},
]

class Command(BaseCommand):
    help = 'Seed complete demo data for Kaamgar Connect'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('\n🌱 Seeding Kaamgar Connect demo data...\n'))

        workers_created = []
        for w in WORKERS:
            user, created = User.objects.get_or_create(
                username=w['username'],
                defaults={
                    'first_name': w['first'], 'last_name': w['last'],
                    'email': w['email'], 'city': w['city'], 'phone': w['phone'],
                    'role': 'worker', 'otp_verified': True, 'bio': w['bio'],
                }
            )
            if created:
                user.set_password('Demo@1234'); user.save()
                wp, _ = WorkerProfile.objects.get_or_create(user=user)
                wp.skills = w['skill']; wp.experience_years = w['exp']
                wp.daily_rate = w['rate']; wp.rating = w['rating']
                wp.availability = True; wp.aadhar_verified = True
                wp.total_jobs = w['total']
                wp.extra_skills = 'Hindi, English, Teamwork'
                wp.save()
                self.stdout.write(f'  ✓ Worker: {user.get_full_name()}')
            workers_created.append(user)

        employers_created = []
        for e in EMPLOYERS:
            user, created = User.objects.get_or_create(
                username=e['username'],
                defaults={
                    'first_name': e['first'], 'last_name': e['last'],
                    'email': e['email'], 'city': e['city'],
                    'role': 'employer', 'otp_verified': True,
                }
            )
            if created:
                user.set_password('Demo@1234'); user.save()
                ep, _ = Employer.objects.get_or_create(user=user)
                ep.company_name = e['company']; ep.industry = e['industry']
                ep.verified = True; ep.save()
                self.stdout.write(f'  ✓ Employer: {user.get_full_name()}')
            employers_created.append(user)

        jobs_created = []
        for j in JOBS:
            employer = employers_created[j['employer_idx'] % len(employers_created)]
            job, created = Job.objects.get_or_create(
                title=j['title'], employer=employer,
                defaults={
                    'category': j['cat'], 'location': j['loc'],
                    'description': j['desc'], 'skills_required': j.get('skills',''),
                    'experience_req': j['exp'],
                    'salary_min': j['smin'], 'salary_max': j['smax'],
                    'job_type': 'full_time', 'openings': 2,
                    'is_active': True, 'is_featured': j.get('featured', False),
                }
            )
            if created:
                self.stdout.write(f'  ✓ Job: {job.title}')
            jobs_created.append(job)

        # Create sample applications
        app_count = 0
        statuses = ['pending','reviewed','shortlisted','accepted','rejected']
        for i, worker in enumerate(workers_created[:5]):
            for j, job in enumerate(jobs_created[:4]):
                if not Application.objects.filter(job=job, worker=worker).exists():
                    Application.objects.create(
                        job=job, worker=worker,
                        status=statuses[(i+j) % len(statuses)],
                        cover_note=f'I am very interested in this position. I have {worker.worker_profile.experience_years} years of relevant experience.',
                    )
                    app_count += 1

        # Create sample saved jobs
        for worker in workers_created[:3]:
            for job in jobs_created[3:6]:
                SavedJob.objects.get_or_create(user=worker, job=job)

        # Create sample reviews
        for i, worker in enumerate(workers_created[:3]):
            for j, employer in enumerate(employers_created[:2]):
                if not Review.objects.filter(reviewer=employer, reviewee=worker).exists():
                    Review.objects.create(
                        reviewer=employer, reviewee=worker,
                        rating=5 - (i % 2), comment='Great worker, very professional and punctual.',
                    )

        self.stdout.write(self.style.SUCCESS(f'''
✅ Demo data seeded!
   Workers:   {len(workers_created)}
   Employers: {len(employers_created)}
   Jobs:      {len(jobs_created)}
   Applications: {app_count}

📋 Login credentials (password: Demo@1234):
   Workers:   rahul_e, suresh_p, amit_c, priya_cook, vikram_s
   Employers: buildright, techcorp, homefix, securepro
'''))
