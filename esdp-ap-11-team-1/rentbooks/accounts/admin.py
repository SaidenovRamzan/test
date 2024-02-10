from django.contrib import admin
from .models import User, UsersEstimates, TelegramUser, Estimation, CompositionTest


admin.site.register(User)
admin.site.register(UsersEstimates)
admin.site.register(TelegramUser)
admin.site.register(Estimation)
admin.site.register(CompositionTest)

