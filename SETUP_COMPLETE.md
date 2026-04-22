# KAAMGAR CONNECT - INSTALLATION & SETUP GUIDE

## Project Overview
**Kaamgar Connect** is a modern Django-based job marketplace platform with:
- Dark theme professional UI
- Distance-based job/worker filtering
- Advanced review and rating system
- Real-time chat interface
- Responsive design for all devices

---

## Prerequisites

### System Requirements
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (venv or virtualenv)
- SQLite3 (default database)
- Modern web browser

### Optional
- MySQL 5.7+ (for production)
- PostgreSQL (for advanced features)
- Redis (for real-time features)

---

## Installation Steps

### 1. Clone the Repository
```bash
cd c:\Users\Hp\OneDrive\Documents\kaamgar_final\kaamgar_final
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### Key Dependencies
```
Django==4.2.0
django-crispy-forms==2.0
Pillow==9.5.0  # Image processing
python-decouple==3.8  # Environment variables
gunicorn==20.1.0  # WSGI server
python-dotenv==1.0.0
geopy==2.3.0  # For distance calculations
celery==5.3.0  # Task queue (optional)
```

### 4. Create `.env` File
Create a file named `.env` in the project root:

```env
# Django Settings
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

# Optional: MySQL Configuration
# DATABASE_ENGINE=django.db.backends.mysql
# DATABASE_NAME=kaamgar_db
# DATABASE_USER=root
# DATABASE_PASSWORD=your_password
# DATABASE_HOST=localhost
# DATABASE_PORT=3306

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# AWS S3 (for file uploads - optional)
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_STORAGE_BUCKET_NAME=

# Google Maps API (for geolocation)
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### 5. Database Setup

#### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

#### Load Sample Data (Optional)
```bash
python manage.py loaddata sample_data.json
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Create Required Directories
```bash
# Windows
mkdir media\profiles
mkdir media\company_logos
mkdir media\worker_resumes
mkdir static\uploads

# macOS/Linux
mkdir -p media/profiles
mkdir -p media/company_logos
mkdir -p media/worker_resumes
mkdir -p static/uploads
```

---

## Running the Development Server

### Start Django Development Server
```bash
python manage.py runserver
```

Open browser and navigate to:
- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### Default Credentials
- **Username**: admin
- **Password**: (whatever you set during createsuperuser)

---

## Project Structure

```
kaamgar_final/
├── accounts/              # User authentication & profiles
├── admin_panel/          # Admin dashboard
├── applications/         # Job applications
├── chat/                 # Real-time messaging
├── dashboard/            # User dashboards
├── employers/            # Employer profiles
├── jobs/                 # Job postings
├── notifications/        # Notification system
├── reviews/              # Review & rating system
├── workers/              # Worker profiles
├── kaamgar_connect/      # Project settings
│   ├── settings.py       # Main configurations
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI application
│   └── asgi.py           # ASGI application
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── dark-theme.css    # Dark theme styles
│   │   └── style.css         # Additional styles
│   └── js/
│       └── main.js           # Main JavaScript
├── media/                # User uploads
│   ├── profiles/         # Profile pictures
│   ├── company_logos/    # Company logos
│   └── worker_resumes/   # Uploaded resumes
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # Auth templates
│   ├── jobs/             # Job templates
│   ├── chat/             # Chat templates
│   └── reviews/          # Review templates
├── manage.py             # Django management
├── requirements.txt      # Dependencies
├── SETUP.md
├── ENHANCEMENTS.md       # New features documentation
└── db.sqlite3            # SQLite database
```

---

## Features Configuration

### Dark Theme
- Already applied by default in `base.html`
- CSS file: `static/css/dark-theme.css`
- Customize colors in CSS variables section

### Distance Filtering
1. Ensure jobs/workers have latitude/longitude
2. Use geolocation in templates:
```html
<button id="distanceFilterBtn" data-bs-toggle="modal">
  Filter by Distance
</button>
```

### Review System
1. Reviews are auto-created after job completion
2. Workers can submit reviews within 7 days
3. Reviews display on worker profile

### Chat System
1. Real-time messaging between users
2. Messages polled every 3 seconds
3. Conversations list available in dashboard

---

## Admin Panel Setup

### Access Admin Panel
1. Go to `http://localhost:8000/admin`
2. Login with superuser credentials
3. Configure:
   - Sites (Domain/Sitename)
   - Users & Permissions
   - Job Categories
   - Worker Skills
   - Employment Types

### Create Test Data

#### Create Test Jobs
```python
python manage.py shell

from jobs.models import Job
from accounts.models import CustomUser

employer = CustomUser.objects.get(username='employer1')
job = Job.objects.create(
    employer=employer,
    title='Plumber Required',
    category='plumbing',
    job_type='daily',
    experience_req='fresher',
    location='Bhopal',
    description='Need a skilled plumber for residential work',
    salary_min=500,
    salary_max=1000,
    latitude=23.1815,
    longitude=79.9864
)
job.save()
```

---

## User Roles & Permissions

### Job Seeker (Worker)
- Register & create profile
- Search & apply for jobs
- Save favorite jobs
- Chat with employers
- Receive review from employers
- Write reviews for jobs completed

### Employer
- Register company
- Post jobs
- View applications
- Accept/reject workers
- Chat with workers
- Rate workers after job completion
- Access analytics dashboard

### Admin
- Manage all users
- Approve/suspend accounts
- Moderate content
- View platform analytics
- Configure settings

---

## Deployment

### Production Settings

#### Update settings.py
```python
# Production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/kaamgar/static/'
MEDIA_ROOT = '/var/www/kaamgar/media/'

# Database (Use MySQL or PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kaamgar_prod',
        'USER': 'kaamgar_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn kaamgar_connect.wsgi -b 0.0.0.0:8000 --workers 4
```

### Using Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /var/www/kaamgar/static/;
    }
    
    location /media/ {
        alias /var/www/kaamgar/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## Testing

### Run Tests
```bash
python manage.py test
```

### Test Specific App
```bash
python manage.py test accounts
python manage.py test jobs
python manage.py test reviews
```

### Test Coverage (Optional)
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution**: Ensure virtual environment is activated
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Issue: Database errors / "no such table"
**Solution**: Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files and check settings
```bash
python manage.py collectstatic --noinput
# Check STATIC_URL and STATIC_ROOT in settings
```

### Issue: Media files not displaying
**Solution**: Ensure media folder exists and check MEDIA_URL/MEDIA_ROOT
```bash
mkdir -p media/profiles
mkdir -p media/company_logos
mkdir -p media/worker_resumes
```

### Issue: Distance filtering not working
**Solution**: Ensure jobs/workers have valid coordinates
```python
# In admin or shell
job.latitude = 23.1815
job.longitude = 79.9864
job.save()
```

### Issue: Email not sending
**Solution**: Configure email backend in settings.py
```python
# Development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

---

## Performance Optimization

### Database Optimization
```python
# Use select_related for foreign keys
jobs = Job.objects.select_related('employer').all()

# Use prefetch_related for many-to-many
workers = Worker.objects.prefetch_related('skills').all()

# Add database indexing
class Job(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['category', 'location']),
        ]
```

### Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def popular_jobs(request):
    return render(request, 'jobs/popular.html')
```

### Static File Optimization
- Minify CSS/JS in production
- Use CDN for static files
- Enable gzip compression in Nginx

---

## Monitoring & Logging

### Setup Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/kaamgar/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Important Files to Customize

### 1. Base Template (`templates/base.html`)
- Update logo/branding
- Modify navbar links
- Update footer information
- Add Google Analytics

### 2. Settings (`kaamgar_connect/settings.py`)
- Change SECRET_KEY
- Configure email
- Set up static/media paths
- Add allowed hosts

### 3. CSS (`static/css/dark-theme.css`)
- Customize color palette
- Modify spacing
- Update typography

### 4. JavaScript (`static/js/main.js`)
- Configure API endpoints
- Update polling intervals
- Customize animations

---

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG = False
- [ ] Use HTTPS (SSL/TLS)
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Set up proper permissions
- [ ] Regular database backups
- [ ] Monitor error logs
- [ ] Keep dependencies updated

---

## Support & Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Enhancement Features](ENHANCEMENTS.md)

### Useful Commands
```bash
# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Shell access
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Check project
python manage.py check

# Clear cache
python manage.py clear_cache
```

---

## Next Steps

1. **Customize**: Update branding and colors
2. **Test**: Test all features locally
3. **Deploy**: Push to production server
4. **Monitor**: Set up error tracking
5. **Promote**: Launch and marketing

---

## Version History

- **v2.0.0** (April 2026): Enhanced with distance filtering, advanced reviews, dark theme
- **v1.0.0** (Baseline): Core functionality

---

## License & Attribution

Developed by Kaamgar Connect Team
© 2025-2026. All rights reserved.

---

**Last Updated**: April 22, 2026  
**For Issues**: Contact support@kaamgar.com
