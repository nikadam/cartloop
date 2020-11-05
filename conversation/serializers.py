from rest_framework import routers, serializers, viewsets
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'payload', 'status', 'conversation', 'user']