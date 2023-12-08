import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chatting.models import ChatRoom, Message
from account.models import Account, OnlineAccount


class ChatConsumer(AsyncWebsocketConsumer):
    def getUser(self, userId):
        return Account.objects.get(id=userId)

    def getOnlineUsers(self):
        onlineUsers = OnlineAccount.objects.all()
        return [onlineUser.account.id for onlineUser in onlineUsers]

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

    def saveMessage(self, message, user_id, room_id):
        userObj = Account.objects.get(id=user_id)
        chatObj = ChatRoom.objects.get(id=room_id)
        chatMessageObj = Message.objects.create(
            chat=chatObj, sender=userObj, text=message
        )
        return {
            'action': 'message',
            'user': user_id,
            'roomId': room_id,
            'message': message,
            'userImage': userObj.image.url,
            'username': userObj.username,
            'created': str(chatMessageObj.created)
        }

    async def sendOnlineUserList(self):
        onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
        chatMessage = {
            'type': 'chat_message',
            'message': {
                'action': 'onlineUser',
                'userList': onlineUserList
            }
        }
        await self.channel_layer.group_send('onlineUser', chatMessage)

    async def connect(self):
        self.userId = self.scope['url_route']['kwargs']['userId']
        self.userRooms = await database_sync_to_async(list)(ChatRoom.objects.filter(users=self.userId))
        for room in self.userRooms:
            await self.channel_layer.group_add(
                str(room.id),
                self.channel_name
            )
        await self.channel_layer.group_add('onlineUser', self.channel_name)
        self.user = await database_sync_to_async(self.getUser)(self.userId)
        await database_sync_to_async(self.addOnlineUser)(self.user)
        await self.sendOnlineUserList()
        await self.accept()

    async def disconnect(self, close_code):
        await database_sync_to_async(self.deleteOnlineUser)(self.user)
        await self.sendOnlineUserList()
        for room in self.userRooms:
            await self.channel_layer.group_discard(
                str(room.id),
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        room_id = text_data_json['roomId']
        chatMessage = {}
        if action == 'message':
            message = text_data_json['message']
            user_id = text_data_json['user']
            chatMessage = await database_sync_to_async(
                self.saveMessage
            )(message, user_id, room_id)
        elif action == 'typing':
            chatMessage = text_data_json
        await self.channel_layer.group_send(
            str(room_id),
            {
                'type': 'chat_message',
                'message': chatMessage
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
