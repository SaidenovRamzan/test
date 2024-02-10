from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import UserShelfSerializer
from rents.models import UserShelf
import logging

class UserShelfApiView(APIView):
    serializer_class = UserShelfSerializer

    def get(self, request):
        query = request.query_params
        user_id, book_id = query.get('user_id'), query.get('book_id')

        if user_id and not book_id:
            user_shelf = UserShelf.objects.filter(user__id=user_id)
            if not user_shelf:
                return Response({'error': 'not found'})
            return Response({i.id_book: {i.user.id: f"id_usershelf = {i.id}"} for i in user_shelf})
        
        elif book_id and not user_id:
            user_shelf = UserShelf.objects.filter(id_book=book_id)
            if not user_shelf:
                return Response({'error': 'not found'})
            return Response({i.id_book: {i.book: f"user_id = {i.user.id}"} for i in user_shelf})
            
        elif book_id and user_id:
            user_shelf = UserShelf.objects.filter(user__id=user_id, id_book=book_id)
            if not user_shelf:
                return Response({'error': 'not found'})
            return Response({i.id: i.id_book for i in user_shelf})
        
        else: 
            return Response({'error': 'don\'t get user_id, book_id'})
        
    def post(self, request):
        logging.info(f'{request.data=}')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_shelf = UserShelf.objects.filter(user__id=request.data.get('user'), id_book=request.data.get('book')).first()
            if user_shelf:
                user_shelf.count += 1
                user_shelf.save()
            else:
                serializer.save()
            return Response('OK')
        return Response({'error': serializer.error_messages})
    
    def delete(self, request):
        query = request.query_params
        user_id, book_id = query.get('user_id'), query.get('book_id')
        if book_id and user_id:
            user_shelf = UserShelf.objects.filter(user__id=user_id, book=book_id).first()
            if not user_shelf:
                return Response({'error': 'not found'})
            user_shelf.delete()
            return Response("ok")
        else: 
            return Response({'error': 'don\'t get user_id, book_id'})