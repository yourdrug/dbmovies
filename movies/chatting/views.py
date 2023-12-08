from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from chatting.serializers import ChatRoomSerializer, ChatMessageSerializer
from chatting.models import ChatRoom, Message


class ChatRoomView(APIView):
    def get(self, request, user_id):
        chatRooms = ChatRoom.objects.filter(users=user_id)
        serializer = ChatRoomSerializer(
            chatRooms, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatRoomSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessagesView(ListAPIView):
    serializer_class = ChatMessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    authentication_classes = (TokenAuthentication,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        roomId = self.kwargs['roomId']
        return Message.objects.filter(chat__id=roomId).order_by('-created')
