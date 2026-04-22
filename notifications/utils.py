from .models import Notification

def notify(user, ntype, title, body='', link=''):
    Notification.objects.create(user=user, ntype=ntype, title=title, body=body, link=link)

def notify_new_application(employer, worker, job):
    notify(
        employer, 'application',
        f'New application for "{job.title}"',
        f'{worker.get_full_name() or worker.username} applied to your job.',
        f'/jobs/{job.pk}/applicants/'
    )

def notify_status_change(worker, job, status):
    status_labels = {'accepted': '✅ Accepted', 'rejected': '❌ Rejected', 'reviewed': '👁 Reviewed'}
    notify(
        worker, 'status',
        f'Application {status_labels.get(status, status)} – {job.title}',
        f'Your application for "{job.title}" has been {status}.',
        '/applications/'
    )

def notify_new_message(recipient, sender):
    notify(
        recipient, 'message',
        f'New message from {sender.get_full_name() or sender.username}',
        'You have a new message waiting.',
        '/chat/'
    )
