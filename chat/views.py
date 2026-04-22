from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.http import JsonResponse
from .models import ChatRoom, Message
from accounts.models import CustomUser

@login_required
def inbox(request):
    user = request.user
    if user.role == 'worker':
        rooms = ChatRoom.objects.filter(worker=user).select_related('employer').prefetch_related('messages')
    else:
        rooms = ChatRoom.objects.filter(employer=user).select_related('worker').prefetch_related('messages')
    return render(request, 'chat/inbox.html', {'rooms': rooms})

@login_required
def room(request, pk):
    current_room = get_object_or_404(ChatRoom, pk=pk)
    user = request.user
    if user != current_room.worker and user != current_room.employer:
        django_messages.error(request, 'Access denied.')
        return redirect('chat:inbox')

    other_user = current_room.employer if user == current_room.worker else current_room.worker

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            msg = Message.objects.create(room=current_room, sender=user, text=text)
            # Notify recipient
            try:
                from notifications.utils import notify_new_message
                notify_new_message(other_user, user)
            except Exception:
                pass
        # Return JSON if AJAX, else redirect (fallback for non-JS)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect('chat:room', pk=pk)

    # Mark incoming as read
    Message.objects.filter(
        room=current_room, is_read=False
    ).exclude(sender=user).update(is_read=True)

    chat_messages = current_room.messages.all().order_by('timestamp')

    if user.role == 'worker':
        all_rooms = ChatRoom.objects.filter(worker=user).select_related('employer').prefetch_related('messages')
    else:
        all_rooms = ChatRoom.objects.filter(employer=user).select_related('worker').prefetch_related('messages')

    return render(request, 'chat/room.html', {
        'current_room': current_room,
        'other_user': other_user,
        'messages': chat_messages,
        'all_rooms': all_rooms,
    })

@login_required
def start_chat(request, user_pk):
    other = get_object_or_404(CustomUser, pk=user_pk)
    user = request.user
    if user == other:
        return redirect('chat:inbox')
    if user.role == 'worker' and other.role == 'employer':
        worker, employer = user, other
    elif user.role == 'employer' and other.role == 'worker':
        worker, employer = other, user
    else:
        django_messages.error(request, 'Cannot start a chat between two users of the same role.')
        return redirect('chat:inbox')
    chat_room, _ = ChatRoom.objects.get_or_create(worker=worker, employer=employer)
    return redirect('chat:room', pk=chat_room.pk)

@login_required
def poll_messages(request, pk):
    """AJAX endpoint: return new messages after a given ID."""
    room = get_object_or_404(ChatRoom, pk=pk)
    user = request.user
    if user != room.worker and user != room.employer:
        return JsonResponse({'error': 'forbidden'}, status=403)
    after_id = int(request.GET.get('after', 0))
    msgs = Message.objects.filter(room=room, id__gt=after_id).order_by('timestamp')
    Message.objects.filter(room=room, is_read=False).exclude(sender=user).update(is_read=True)
    data = [{
        'id': m.id,
        'text': m.text,
        'mine': m.sender == user,
        'time': m.timestamp.strftime('%H:%M'),
        'initial': (m.sender.first_name[:1] or m.sender.username[:1]).upper(),
    } for m in msgs]
    return JsonResponse({'messages': data})
