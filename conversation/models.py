from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(
                max_length=50,
                null=True,
                blank=True
            )
    is_operator = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    def __str__(self):
        if self.username:
            return f"{self.username}"
        return f"{self.name}"


class Store(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Client(models.Model):
    user = models.OneToOneField(
                'User',
                on_delete=models.CASCADE,
                primary_key=True
            )

    def __str__(self):
        return f"{self.user.name}"


class Operator(models.Model):
    user = models.OneToOneField(
                'User',
                on_delete=models.CASCADE,
                primary_key=True
            )
    group = models.ForeignKey(
                'Group',
                related_name='operators',
                on_delete=models.CASCADE
            )

    def __str__(self):
        return f"{self.user.name}({self.group})"


class Conversation(models.Model):
    store = models.ForeignKey(
                'Store',
                on_delete=models.CASCADE
            )
    operator = models.ForeignKey(
                'User',
                on_delete=models.CASCADE,
                related_name='operator_conversations'
            )
    client = models.ForeignKey(
                'User',
                on_delete=models.CASCADE,
                related_name='client_conversations'
            )

    def __str__(self):
        return f"""Conversation between {self.operator}
        and {self.client} for store {self.store}"""


class Chat(models.Model):
    NEW = 'N'
    SENT = 'S'
    STATUS_CHOICES = [
        (NEW, 'New'),
        (SENT, 'Sent'),
    ]
    from django.core.validators import RegexValidator
    payload = models.CharField(
                max_length=300,
                validators=[
                    RegexValidator(
                        regex='^[a-zA-Z0-9\{\}$%_\-\/~@#$%^&*()!? ]*$',
                        message='Message must be Alphanumeric or must have any of these special char({}$%_-/~@#$%^&*()!?)',
                        code='invalid_payload'
                    )
                ])
    status = models.CharField(
                max_length=1,
                choices=STATUS_CHOICES,
                default=NEW
            )
    conversation = models.ForeignKey(
                    'Conversation',
                    on_delete=models.CASCADE,
                    related_name='chats'
                )
    user = models.ForeignKey(
                'User',
                on_delete=models.CASCADE,
                related_name='user_chats'
            )
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation}"


class ScheduleChat(models.Model):
    conversation = models.ForeignKey(
                    'Conversation',
                    on_delete=models.CASCADE,
                    related_name='schedule_chats'
                )
    chat = models.ForeignKey(
                'Chat',
                on_delete=models.CASCADE,
                related_name='schedule_chats'
            )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation}"
