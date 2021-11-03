from django.urls import re_path

from . import consumers, consumerboat

websocket_urlpatterns = [
    re_path('ws/chat/', consumers.ChatConsumer.as_asgi()),
    re_path('ws/boat/', consumerboat.ChatConsumer.as_asgi()),
]