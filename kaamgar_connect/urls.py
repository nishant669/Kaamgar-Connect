from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'kaamgar_connect.views.page_not_found'
handler500 = 'kaamgar_connect.views.server_error'

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('',              include('accounts.urls',       namespace='accounts')),
    path('dashboard/',    include('dashboard.urls',      namespace='dashboard')),
    path('jobs/',         include('jobs.urls',            namespace='jobs')),
    path('workers/',      include('workers.urls',         namespace='workers')),
    path('employers/',    include('employers.urls',       namespace='employers')),
    path('applications/', include('applications.urls',   namespace='applications')),
    path('chat/',         include('chat.urls',            namespace='chat')),
    path('reviews/',      include('reviews.urls',         namespace='reviews')),
    path('notifications/',include('notifications.urls',  namespace='notifications')),
    path('manage/',       include('admin_panel.urls',     namespace='admin_panel')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
