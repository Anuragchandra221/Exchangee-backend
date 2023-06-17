import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import base64
class chatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({
            'type':"connection",
            "message": "hello world"
        }))


    def receive(self, bytes_data):
        # binary_data = base64.b64decode(bytes_data)
        print(type(bytes_data))
        # binary_data = text_data.encode('utf-8')
        # text_data_json = json.loads(text_data)
        print("receive")
        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'file_message',
                    'message': bytes_data,
                }
            )
    
    def file_message(self, event):
        file_data = event['message']
        self.send(bytes_data=file_data)

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
        }))
