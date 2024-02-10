from chat.models import Chat, Message
from asgiref.sync import sync_to_async


class ChatServices:
    @classmethod
    def sync_get_chat_or_create(cls, user_1: int, user_2: int, user_shelf: int):
        chat = cls._get_chat_or_create(user_1, user_2, user_shelf)
        return chat
    
    @classmethod
    async def async_get_chat_or_create(cls, user_1: int, user_2: int, user_shelf: int):
        chat = await sync_to_async(cls._get_chat_or_create)(user_1, user_2, user_shelf)
        return chat

    @classmethod
    def _get_chat_or_create(cls, user_1: int, user_2: int, user_shelf: int):
        chat = Chat.objects.filter(
            user_1=user_1, 
            user_2=user_2,
            user_shelf=user_shelf
        ).first() or Chat.objects.filter(
            user_1=user_2, 
            user_2=user_1,
            user_shelf=user_shelf
        ).first()
        if chat:
            return chat
        else:
            return Chat.objects.create(user_1=user_1, user_2=user_2, user_shelf=user_shelf)
        
    @classmethod
    def get_all_chats(cls, user_id: int) -> list:
        chats_1 = Chat.objects.filter(user_1=user_id)
        chats_2 = Chat.objects.filter(user_2=user_id)
        chats_ids = []
        [chats_ids.append(chat.id) for chat in chats_1]
        [chats_ids.append(chat.id) for chat in chats_2]
        return chats_ids
    

class MessageServises:
    @classmethod
    async def create_message(cls, chat: Chat, sender_id: int, recipient_id: int, message: str):
        user_shelf_id = chat.user_shelf
        return await sync_to_async(Message.objects.create)(
            chat = chat,
            sender = sender_id,
            recipient = recipient_id,
            user_shelf = user_shelf_id,
            message=message
        )
        
    @classmethod
    def get_messages(cls, chat):
        messages = Message.objects.filter(chat=chat)
        messages = messages.order_by('created_at')
        message_list = list(messages)
        return message_list
