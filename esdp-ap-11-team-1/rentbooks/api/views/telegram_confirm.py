import random
import requests
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.cache import cache
from django.db.models import Q

from accounts.models import TelegramUser
from accounts.models import User
import logging


class TelegramConfirm(APIView):
    model = TelegramUser
    
    def post(self, request, *args, **kwargs):
        user_id = int(request.data.get('user_id'))
        telegram_id = request.data.get('telegram_id')
        try:
            telegram_user = self.get_or_create(id_user=user_id, id_telegram=telegram_id)
            if telegram_user.confirm:
                code = "Вы уже подтвердили Telegram"
            else: 
                code = random.randint(10000, 999999)
        except NotImplementedError:
            return JsonResponse({'error': 'Telegram id was coneccted'}, status=404)
        
        bot_token = '6828045583:AAFF2kuNgxOlC7KSP6cQKXQjYkNke4RXu48'
        target_chat_id = telegram_id
        cache.set(user_id, code, timeout=60)
        telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': target_chat_id,
            'text': code,
        }
        response = requests.post(telegram_api_url, data=payload)
        return JsonResponse({'OK': 123}, status=200)

    def get_or_create(self, id_user, id_telegram) -> TelegramUser:
        telegram_user = TelegramUser.objects.filter(user__id=id_user).exists()
        if TelegramUser.objects.filter(id_telegram=id_telegram).exists():
            if not TelegramUser.objects.filter(id_telegram=id_telegram, user__id=id_user).exists():
                raise NotImplementedError
            
        elif not telegram_user:
            telegram_user = self.model(
                user=User.objects.get(id=id_user),
                id_telegram=id_telegram
            )
            telegram_user.save()
            return telegram_user
        
        elif telegram_user:
            logging.info('retern')
            return TelegramUser.objects.filter(user__id=id_user).first()
            
            
class TelegramCode(APIView):
    def post(self, request, *args, **kwargs):
        user_id = int(request.data.get('user_id'))
        code = request.data.get('code')
        value = cache.get(user_id)
        
        if str(value) == code:
            telegram_user = TelegramUser.objects.filter(user__id=user_id).first()
            if telegram_user.confirm:
                text = "Вы уже подтвердили Telegram"
            else:
                text = "Вы успешно подтвердили Telegram"
                
            telegram_user.confirm = True
            telegram_user.save()
            
            bot_token = '6828045583:AAFF2kuNgxOlC7KSP6cQKXQjYkNke4RXu48'
            telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            
            payload = {
                'chat_id': telegram_user.id_telegram,
                'text': text,
            }
            response = requests.post(telegram_api_url, data=payload)
        
            return JsonResponse({'OK': 200})
        return JsonResponse({'error': "code dont confirm"})
    