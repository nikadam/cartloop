from rest_framework import routers, serializers, viewsets
from .models import Chat, Conversation

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "payload", "status", "conversation", "user"]


class ConversationSerializer(serializers.ModelSerializer):
    operatorGroup = serializers.SerializerMethodField()
    chats = ChatSerializer(many=True)

    class Meta:
        model=Conversation
        fields = ["id", "store", "operator", "client", 'operatorGroup', 'chats']

    def get_operatorGroup(self, request):
        return self.instance.operator.operator.group.name