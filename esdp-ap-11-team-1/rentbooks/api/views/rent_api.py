import django
from rest_framework.views import APIView
from django.http import JsonResponse
import random
import logging
from rents.models import OrderOfRent
from rents.models import UserShelf
from books.models import Book, Composition
from django.shortcuts import get_object_or_404
from chat.services import ChatServices
from accounts.models import TelegramUser
import requests


class CreateOrder(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        usershelf_id = request.data.get('composition_id')
        date_plan_start = request.data.get('date_plan_start')
        date_plan_end = request.data.get('date_plan_end')
        purpose = request.data.get('purpose')
        order_code = random.randint(1000, 9999)
        usershelf = get_object_or_404(UserShelf, id=usershelf_id)

        if str(purpose) == 'buy':
            if usershelf.purpose not in ['sale', 'rent and sale']:
                return JsonResponse({'error': 'Книга не продается'}, status=400)
        elif str(purpose) == 'rent':
            if usershelf.purpose not in ['rent', 'rent and sale']:
                return JsonResponse({'error': 'Книга не арендуется'}, status=400)

        if usershelf.user_id == int(user_id):
            return JsonResponse({'error': 'Вы не можете отправлять заявку себе'}, status=400)
        else:
            order = OrderOfRent.objects.create(
                user_id=user_id,
                usershelf_id=usershelf_id,
                date_plan_start=date_plan_start,
                date_plan_end=date_plan_end,
                number_for_owner=order_code,
                purpose=purpose
            )
            text = "У вас новый заказ\n"
            try:
                user_id_for_TG = UserShelf.objects.select_related('user').get(id=usershelf_id).user.id
                telegram_user = TelegramUser.objects.filter(user__id=user_id_for_TG).first()
                bot_token = '6828045583:AAFF2kuNgxOlC7KSP6cQKXQjYkNke4RXu48'
                telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

                payload = {
                    'chat_id': telegram_user.id_telegram,
                    'text': text,
                }
                response = requests.post(telegram_api_url, data=payload)
            except:
                pass
            return JsonResponse({'id': order.id}, status=200)


class StartFactRent(APIView):
    def post(self, request, *args, **kwargs):
        numbers = request.data.get('numbers')
        order = OrderOfRent.objects.get(id=kwargs.get('pk'))
        logging.info(numbers)
        logging.info(order.number_for_owner)
        if not str(numbers).isdigit():
            return JsonResponse({'error': 'Неверный формат'}, status=400)            
        elif order.number_for_owner == int(numbers):
            if order.purpose == 'buy':
                order.date_fact_end = django.utils.timezone.now()
                order.is_active = False
                order.is_finished = True
                order.number_for_owner = order.number_for_renter = None
                order.save()
                usershelf = order.usershelf
                usershelf.count -= 1
                if usershelf.count == 0:
                    usershelf.status = 'sold'
                    usershelf.save()
                    return JsonResponse({'id': order.id}, status=200)
                else:
                    usershelf.status = 'available'
                    usershelf.save()
                    return JsonResponse({'id': order.id}, status=200)
            else:
                order.date_fact_start=django.utils.timezone.now()
                code = random.randint(1000, 9999)
                order.number_for_renter = code
                order.save()
                usershelf = order.usershelf
                usershelf.count -= 1
                if usershelf.count == 0:
                    usershelf.status = 'in_rent'
                    usershelf.save()
                    return JsonResponse({'id': order.id}, status=200)
                else:
                    usershelf.status = 'available'
                    usershelf.save()
                    return JsonResponse({'id': order.id}, status=200)
        else:
            return JsonResponse({'error': 'Неверный код'}, status=400)
            
            
class FinishFactRent(APIView):
    def post(self, request, *args, **kwargs):
        numbers = request.data.get('numbers')
        date = django.utils.timezone.now()

        rent = OrderOfRent.objects.get(id=kwargs.get('pk'))
        if not str(numbers).isdigit():
            return JsonResponse({'error': 'Неверный формат'}, status=400)
        elif rent.number_for_renter == int(numbers) and rent.date_fact_start:
            rent.date_fact_end = date
            rent.number_for_owner = rent.number_for_renter = None
            rent.is_active = False
            rent.is_finished = True
            rent.save()
            usershelf = rent.usershelf
            usershelf.count += 1
            usershelf.status = 'available'
            usershelf.save()
            bookid = usershelf.id_book
            book = Book.objects.get(id_Book=bookid)
            compositionid = book.id_composition.id
            compostion = Composition.objects.get(id_Composition=compositionid)
            compostion.rent_qte += 1
            compostion.save()
            return JsonResponse({'id': rent.id}, status=200)
        else:
            return JsonResponse({'error': 'Неверный код'}, status=400)


class ApproveOrder(APIView):
    def post(self, request, *args, **kwargs):
        order = OrderOfRent.objects.get(id=kwargs.get('pk'))
        order.is_approved=True
        order.save()
        usershelf = order.usershelf
        usershelf.status = 'reserved'
        usershelf.save()
        id1 = order.user.id
        id2 = order.usershelf.user.id
        user_shelf_id = order.usershelf.id
        chat = ChatServices.sync_get_chat_or_create(user_1=int(id1), user_2=int(id2), user_shelf=int(user_shelf_id))
        return JsonResponse({'id': order.id}, status=200)


class DeclineOrder(APIView):
    def post(self, request, *args, **kwargs):
        order = OrderOfRent.objects.get(id=kwargs.get('pk'))
        order.is_approved=False
        order.is_active=False
        order.is_finished=True
        order.save()
        return JsonResponse({'id': order.id}, status=200)


class CancelOrder(APIView):
    def post(self, request, *args, **kwargs):
        order = OrderOfRent.objects.get(id=kwargs.get('pk'))
        order.is_active=False
        order.is_finished=True
        order.save()
        return JsonResponse({'id': order.id}, status=200)
