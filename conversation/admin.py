from django.contrib import admin
from .models import User, Store, Group, Client, Operator, Conversation, Chat, ScheduleChat


admin.site.register(User)
admin.site.register(Store)
admin.site.register(Group)
admin.site.register(Client)
admin.site.register(Operator)
admin.site.register(Conversation)
admin.site.register(Chat)
admin.site.register(ScheduleChat)