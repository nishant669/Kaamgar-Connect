from django.urls import path
from . import views
app_name = 'jobs'
urlpatterns = [
    path('',                   views.job_list,       name='list'),
    path('<int:pk>/',           views.job_detail,     name='detail'),
    path('post/',               views.post_job,       name='post'),
    path('<int:pk>/edit/',      views.edit_job,       name='edit'),
    path('my-jobs/',            views.my_jobs,        name='my_jobs'),
    path('<int:pk>/applicants/',views.job_applicants, name='applicants'),
    path('<int:pk>/toggle/',    views.toggle_job,     name='toggle'),
    path('<int:pk>/delete/',    views.delete_job,     name='delete'),
    path('<int:pk>/save/',      views.toggle_save_job,name='save'),
    path('saved/',              views.saved_jobs,     name='saved'),
]
