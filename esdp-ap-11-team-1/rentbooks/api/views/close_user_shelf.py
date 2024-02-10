from django.shortcuts import redirect
from rest_framework.views import APIView
import logging
from rents.models import UserShelf


class CloseUserShelf(APIView):
    def get(self, request, *args, **kwargs):
        logging.info(kwargs.get("pk"))
        user_shelf = UserShelf.objects.get(id=kwargs.get("pk"))
        if self.request.user.id == UserShelf.objects.select_related('user').get(id=user_shelf.id).user.id:
            user_shelf.is_active = False
            user_shelf.save()
        return redirect('user_profile')