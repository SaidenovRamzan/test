from django.db import models
from django.contrib.auth import get_user_model
import django


class Comment(models.Model):
    
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=get_user_model(),
        related_name='comments',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    composition_id = models.BigIntegerField(
        null=False,
        blank=False,
        default=0
    )

    text = models.CharField(
        verbose_name='Комментарий',
        null=False,
        blank=False,
        max_length=200
    )

    date_publish = models.DateTimeField(
        default=django.utils.timezone.now,
        verbose_name='Дата публикации')