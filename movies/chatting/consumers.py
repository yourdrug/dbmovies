import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from enum import Enum
from channels.generic.websocket import AsyncWebsocketConsumer
from chatting.models import ChatRoom, Message
from account.models import Account, OnlineAccount, Guest


class SocketActions(Enum):
    MESSAGE = 'message'
    TYPING = 'typing'
    ONLINE_USER = 'onlineUser'


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_chat_id = 3

    def getUser(self, user_id):
        return Account.objects.get(id=user_id)

    def getOnlineUsers(self):
        onlineUsers = list(OnlineAccount.objects.values_list('account_id', flat=True))
        return onlineUsers

    def addOnlineUser(self, account):
        try:
            OnlineAccount.objects.create(account=account)
        except:
            pass

    def deleteOnlineUser(self, account):
        try:
            OnlineAccount.objects.get(account=account).delete()
        except:
            pass

    @database_sync_to_async
    def add_to_global_chat_if_not_exists(self, user, global_chat_id):
        global_chat_room = ChatRoom.objects.prefetch_related('users').filter(id=global_chat_id).first()
        if global_chat_room and user not in global_chat_room.users.all():
            global_chat_room.users.add(user)

    def saveMessage(self, message, user_id, room_id):
        user_obj = Account.objects.get(id=user_id)
        chat_obj = ChatRoom.objects.get(id=room_id)
        chat_message_obj = Message.objects.create(
            chat=chat_obj, sender=user_obj, text=message
        )
        return {
            'action': SocketActions.MESSAGE.value,
            'sender': user_id,
            'roomId': room_id,
            'text': message,
            'userImage': user_obj.image.url,
            'username': user_obj.username,
            'created': str(chat_message_obj.created)
        }

    async def sendOnlineUserList(self):
        online_user_list = await database_sync_to_async(self.getOnlineUsers)()
        chat_message = {
            'type': 'chat_message',
            'message': {
                'action': SocketActions.ONLINE_USER.value,
                'userList': online_user_list
            }
        }
        await self.channel_layer.group_send('onlineUser', chat_message)

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['userId']
        self.user = await database_sync_to_async(self.getUser)(self.user_id)

        await self.add_to_global_chat_if_not_exists(user=self.user, global_chat_id=3)

        self.user_rooms = await database_sync_to_async(list)(ChatRoom.objects.filter(users=self.user_id))
        for room in self.user_rooms:
            await self.channel_layer.group_add(
                str(room.id),
                self.channel_name
            )
        await self.channel_layer.group_add('onlineUser', self.channel_name)

        await database_sync_to_async(self.addOnlineUser)(self.user)
        await self.sendOnlineUserList()
        await self.send_online_users_count()
        await self.accept()

    async def disconnect(self, close_code):
        await database_sync_to_async(self.deleteOnlineUser)(self.user)
        await self.sendOnlineUserList()
        await self.send_online_users_count()
        for room in self.user_rooms:
            await self.channel_layer.group_discard(
                str(room.id),
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        room_id = text_data_json['roomId']
        chat_message = {}
        if action == SocketActions.MESSAGE.value:
            message = text_data_json['message']
            user_id = text_data_json['user']
            chat_message = await database_sync_to_async(self.saveMessage)(message, user_id, room_id)
        elif action == SocketActions.TYPING.value:
            chat_message = text_data_json
        await self.channel_layer.group_send(
            str(room_id),
            {
                'type': 'chat_message',
                'message': chat_message
            }
        )

    @database_sync_to_async
    def get_online_users(self):
        online_users = OnlineAccount.objects.count()
        online_guests = Guest.objects.count()
        return online_users + online_guests

    async def send_online_users_count(self):
        online_users_count = await self.get_online_users()

        chat_message = {
            'type': 'online_users_count',
            'message': {
                'action': 'online_users_count',
                'count': online_users_count
            }
        }
        await self.channel_layer.group_send('onlineUser', chat_message)

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def online_users_count(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))


class GuestConsumer(AsyncWebsocketConsumer):
    room_id = 'global_chatroom'

    @database_sync_to_async
    def add_guest(self):
        try:
            Guest.objects.create(name="Guest")
        except:
            pass

    @database_sync_to_async
    def delete_guest(self):
        try:
            Guest.objects.first().delete()
        except:
            pass

    async def connect(self):
        self.room_group_name = f"chat_{self.room_id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.add_guest()
        await self.send_online_users_count()

        await self.accept()

    async def disconnect(self, close_code):
        await self.delete_guest()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.send_online_users_count()

    @database_sync_to_async
    def get_online_users(self):
        online_users = OnlineAccount.objects.count()
        online_guests = Guest.objects.count()
        return online_users + online_guests

    async def send_online_users_count(self):
        online_users_count = await self.get_online_users()

        chat_message = {
            'type': 'online_users_count',
            'message': {
                'action': 'online_users_count',
                'count': online_users_count
            }
        }
        await self.channel_layer.group_send(self.room_group_name, chat_message)

    async def online_users_count(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
