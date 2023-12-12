from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class ChatRoomTypes(models.TextChoices):
    GLOBAL = "GLOBAL", _("Общий чат")
    DIRECTMESSAGES = "DM", _("Личные сообщения")
    SELF = "SELF", _("Сохранённое")


class ChatRoom(models.Model):
    name = models.CharField(max_length=30, null=False)
    type = models.CharField(max_length=15, choices=ChatRoomTypes.choices, default=ChatRoomTypes.DIRECTMESSAGES)
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(User, related_name='user_chats')

    class Meta:
        unique_together = ['name', 'type']

    def __str__(self):
        return f'{self.name} --> {self.type}'


class Message(models.Model):
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, null=True)

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_messages')
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='chat_messages')

    def __str__(self):
        return f'{self.sender} --> {self.text}'
