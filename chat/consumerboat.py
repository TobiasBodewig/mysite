import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'chat_boat'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            'chat_boat',
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            'chat_console',
            {
                'type': 'chat_message',
                'message': '[Server]  Boat connected'
            }
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            'chat_boat',
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            'chat_console',
            {
                'type': 'chat_message',
                'message': '[Server]  Boat disconnected'
            }
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # Send message to room group
        if text_data == '-ping-':
            return
        async_to_sync(self.channel_layer.group_send)(
            'chat_console',
            {
                'type': 'chat_message',
                'message': '[Boat]    ' + text_data
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=message)