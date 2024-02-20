import random
import django
import logging
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Q

from rents.models import OrderOfRent, UserShelf
from accounts.models import TelegramUser, User
from books.models import Book, Composition
from chat.services import ChatServices
from chat.models import Chat


class GetAllOrders(APIView):
    model =  OrderOfRent
    
    def post(self, request, *args, **kwargs):
        id_telegram = request.data.get('id')
        telegram_user = TelegramUser.objects.select_related('user').get(id_telegram=id_telegram)
        try:
            user = telegram_user.user
            orders = self.model.objects.select_related('usershelf').filter(~Q(is_approved=False), user=user, is_active=True)
            
            return JsonResponse({"orders": [
                {
                    'id': order.id,
                    'name': Book.objects.get(id_Book=order.usershelf.id_book).id_composition.name,
                    'code' : order.number_for_owner,
                    'is_approved' : order.is_approved,
                    'is_started' : order.date_fact_start,
                    }  for order in orders
                ]})
            
        except TelegramUser.DoesNotExist:
            return JsonResponse({'error': 'Вы не привязали Telegram'}, status=404)
     
        
class GetAllMyOrders(APIView):
    model = OrderOfRent
    
    def post(self, request, *args, **kwargs):
        id_telegram = request.data.get('id')
        telegram_user = TelegramUser.objects.select_related('user').get(id_telegram=id_telegram)
        try:
            user = telegram_user.user
            user_shelfs = UserShelf.objects.select_related('user').filter(user=user)
            orders = self.model.objects.select_related('usershelf').filter(~Q(is_approved=False), usershelf__in=user_shelfs, is_active=True, date_fact_end=None).order_by('-date_create')[:5]
            return JsonResponse({"orders": [
                {
                    'id': order.id,
                    'name': Book.objects.get(id_Book=order.usershelf.id_book).id_composition.name,
                    'start': order.date_plan_start,
                    'end': order.date_plan_end,
                    'code' : order.number_for_owner,
                    'is_approved' : order.is_approved,
                    'is_started' : order.date_fact_start,
                    'is_ended' : order.date_fact_end,
                    
                    } for order in orders
                ]})
        except TelegramUser.DoesNotExist:
            return JsonResponse({'error': 'Вы не привязали Telegram'}, status=404)
        
        
class TelegramStartFactRent(APIView):
    def post(self, request, *args, **kwargs):
        order = OrderOfRent.objects.get(id=kwargs.get('pk'))
        if order.purpose == 'buy':
            order.date_fact_end = django.utils.timezone.now()
            order.is_finished = True
            order.number_for_owner = order.number_for_renter = None
            order.save()
            usershelf = order.usershelf
            usershelf.count -= 1
            usershelf.status = 'sold'
            usershelf.save()
            return JsonResponse({'id': order.id}, status=200)
        else:
            order.date_fact_start=django.utils.timezone.now()
            code = random.randint(1000, 9999)
            order.number_for_renter = code
            order.save()
            usershelf = order.usershelf
            usershelf.status = 'in_rent'
            usershelf.save()
            return JsonResponse({'id': order.id}, status=200)


class TelegramFinishFactRent(APIView):
    def post(self, request, *args, **kwargs):
        date = django.utils.timezone.now()
        rent = OrderOfRent.objects.get(id=kwargs.get('pk'))
        rent.date_fact_end = date
        rent.number_for_owner = rent.number_for_renter = None
        rent.is_finished = True
        rent.save()
        usershelf = rent.usershelf
        usershelf.status = 'available'
        usershelf.save()
        bookid = usershelf.id_book
        book = Book.objects.get(id_Book=bookid)
        compositionid = book.id_composition.id
        compostion = Composition.objects.get(id_Composition=compositionid)
        compostion.rent_qte += 1
        compostion.save()
        return JsonResponse({'id': rent.id}, status=200)
    

class GetAllChats(APIView):
    def get(self, request, *args, **kwargs):
        tg_id = kwargs.get('pk')
        user = TelegramUser.objects.select_related('user').get(id_telegram=int(tg_id)).user
        chat_ids = ChatServices.get_all_chats(user.id)
        chats = [Chat.objects.get(id=id) for id in chat_ids]
        response = [
            {
                'user_id':chat.user_1 if chat.user_1 != user.id else chat.user_2,
                'self_id':chat.user_1 if chat.user_1 == user.id else chat.user_2,
                'chat_id': chat.id,
                'id': chat.id,
                'user_shelf_id': chat.user_shelf,
                'user_shelf_name': Book.objects.get(id_Book=UserShelf.objects.get(id=chat.user_shelf).id_book).id_composition.name,
                'user_name': User.objects.get(id=chat.user_1).username if chat.user_1 != user.id else User.objects.get(id=chat.user_2).username,
                }
            for chat in chats]
        return JsonResponse({'orders': response})
        