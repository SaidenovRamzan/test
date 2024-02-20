from rest_framework.views import APIView
from rest_framework.response import Response

from chat.services import ChatServices, MessageServises
from chat.models import Chat


class ChatAPIView(APIView):
    def post(self, request):
        id1 = request.data.get('id1')
        id2 = request.data.get('id2')
        user_shelf_id = request.data.get('user_shelf')
        if id1 is not None and id2 is not None:
            
            chat = Chat.objects.filter(user_1=id1, user_2=id2, user_shelf=user_shelf_id).first() or Chat.objects.filter(user_1=id2, user_2=id1, user_shelf=user_shelf_id).first()
            masseges_new = MessageServises.get_messages(chat)
            message_list = [{"sender": message.sender, "message": message.message, "time" : message.created_at}\
            for message in masseges_new]
            
            return Response(
                {
                'messages': message_list,
                'many': 1
                }
            )
        else:
            return Response({'error': 'Both id1 and id2 must be provided in the request body'}, status=400)
        
        
class ChatCreateAPIView(APIView):
    def post(self, request):
        id1 = request.data.get('id1')
        id2 = request.data.get('id2')
        user_shelf_id = request.data.get('user_shelf_id')
        
        if id1 is not None and id2 is not None:
            
            chat = ChatServices.sync_get_chat_or_create(user_1=int(id1), user_2=int(id2), user_shelf=int(user_shelf_id))
            if not chat:
                chat = Chat.objects.create(user_1=id2, user_2=id2, user_shelf=user_shelf_id)
            return Response(
                {
                'user_1': chat.user_1,
                'user_': chat.user_2,
                'user_shelf': chat.user_shelf,
                'many': 1
                }
            )
        else:
            return Response({'error': 'Both id1 and id2 must be provided in the request body'}, status=400)