def global_context(request):
    """Inject unread notification count into every template."""
    unread_notifications = 0
    if request.user.is_authenticated:
        try:
            from notifications.models import Notification
            unread_notifications = Notification.objects.filter(
                user=request.user, is_read=False
            ).count()
        except Exception:
            pass
    return {'unread_notifications': unread_notifications}
