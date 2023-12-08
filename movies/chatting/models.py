from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class ChatRoom(models.Model):
    name = models.CharField(max_length=30, null=False)
    type = models.CharField(max_length=10, default='DM')
    users = models.ManyToManyField(User, related_name='user_chats')

    def __str__(self):
        return f'{self.name} --> {self.type}'


class Message(models.Model):
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, null=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages')

    def __str__(self):
        return f'{self.sender} --> {self.text}'
