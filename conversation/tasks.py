from django.core.mail import send_mail
from datetime import datetime
from celery import shared_task

from .models import Chat, Conversation

NEW = 'N'
SENT = 'S'

@shared_task(bind=True,
             name='send_emails',
             max_retries=3)
def send_emails(total):
    if 9 < datetime.now().hour < 20:
        for conv in Conversation.objects.filter(chats__status=NEW).distinct():
            for chat in Chat.objects.filter(conversation=conv, status=NEW).order_by('create_at')[:90]:
                send_mail(
                    'Notification for chat',
                    chat.payload,
                    chat.user.email,
                    [chat.conversation.operator.email if chat.conversation.client.id == chat.user.id else chat.conversation.operator.email],
                    fail_silently=False
                )
                chat.status = SENT
                chat.save()