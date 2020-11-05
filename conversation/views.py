from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status

from .models import Chat, Conversation, ScheduleChat
from .serializers import ChatSerializer


class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def retrieve(self, request, pk=None):
        try:
            chat = self.queryset.get(pk=pk)
        except:
            return Response({"message": "Chat not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "conversationId": chat.conversation.id,
            "chat": {
                "payload": chat.payload,
                "user": chat.user.id
            }
        })
        
    def create(self, request):
        conversationId = request.data.get("conversationId")
        if conversationId:
            try:
                conversation = Conversation.objects.get(pk=conversationId)
            except:
                return Response({"message": "Conversation not found"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["conversation"] = conversation.id
            request.data["payload"] = request.data.get("chat", {}).get("payload")
            request.data["user"] = request.data.get("chat", {}).get("user")
        else:
            return Response({"message": "Conversation Id not found"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)