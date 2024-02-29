from django.urls import re_path
from chatting import consumers

websocket_urlpatterns = [
    re_path(r'ws/users/(?P<userId>\w+)/chat/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/guest/$', consumers.GuestConsumer.as_asgi()),
]
