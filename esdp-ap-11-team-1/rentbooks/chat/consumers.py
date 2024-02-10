# myapp/consumers.py
import json
import aiohttp
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.services import ChatServices, MessageServises
from accounts.models import TelegramUser, User
import logging



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.recipient_id = self.scope['url_route']['kwargs']['recipient_id']
        self.user_shelf_id = self.scope['url_route']['kwargs']['user_shelf_id']
        
        self.chat = await ChatServices.async_get_chat_or_create(int(self.sender_id), int(self.recipient_id), int(self.user_shelf_id))
        self.room_group_name = f"chat_{self.chat.id}"

        # Присоединение к комнате
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от комнаты
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # сохранение в бд сообщения
        message = await MessageServises.create_message(self.chat, self.sender_id, self.recipient_id, message)
        # Отправка сообщения в комнату
        message = {"sender": message.sender, "message": message.message, "time": str(message.created_at.time())}
        try:
            api_token = '6828045583:AAFF2kuNgxOlC7KSP6cQKXQjYkNke4RXu48'
            chat_id = await sync_to_async(TelegramUser.objects.select_related('user').get)(user__id=int(self.recipient_id))
            name = await sync_to_async(User.objects.get)(id=self.sender_id)
            async with aiohttp.ClientSession() as session:
                params = {
                        'chat_id': chat_id.id_telegram,
                        'text': f"{name.username} \nСообщение: {text_data_json['message']}",
                    }
                async with session.post(f'https://api.telegram.org/bot{api_token}/sendMessage', data=params) as response:
                    pass
        except:
            pass
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']
        many = event.get('many', 0)

        await self.send(text_data=json.dumps({
            'message': message,
            'many': many,
            }))
        
    
