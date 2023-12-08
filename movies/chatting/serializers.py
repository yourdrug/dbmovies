from rest_framework import serializers
from chatting.models import ChatRoom, Message
from account.serializers import CurrentUserInfoSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    users = CurrentUserInfoSerializer(many=True, read_only=True)
    members = serializers.ListField(write_only=True)

    def create(self, validatedData):
        memberObject = validatedData.pop('members')
        chatRoom = ChatRoom.objects.create(**validatedData)
        chatRoom.users.set(memberObject)
        return chatRoom

    class Meta:
        model = ChatRoom
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    userImage = serializers.ImageField(source='sender.image')

    class Meta:
        model = Message
        fields = '__all__'

    def get_username(self, obj):
        return obj.sender.username
