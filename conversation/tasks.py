from datetime import datetime
from celery import shared_task

from .models import Chat, Conversation

NEW = 'N'
SENT = 'S'

@shared_task(bind=True,
             name='send_emails',
             max_retries=3,
             soft_time_limit=20)
def send_emails(total):
    if 9 < datetime.now().hour < 20:
        conversations = Conversation.objects.filter(chats__status=NEW).distinct()
        for conv in conversations:
            chat_ids = Chat.objects.filter(conversation=conv, status=NEW).order_by('create_at')[:90].values_list('id', flat=True)
            Chat.objects.filter(id__in=chat_ids).update(status=SENT)