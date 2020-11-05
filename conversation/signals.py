from .models import Chat, ScheduleChat
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Chat)
def schedule_chat(sender, instance, **kwargs):
    ScheduleChat.objects.create(conversation=instance.conversation, chat=instance)
