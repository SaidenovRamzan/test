from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Rating(models.Model):
    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=get_user_model(),
        related_name='ratings',
        on_delete=models.CASCADE
    )
    composition_id = models.BigIntegerField(
        verbose_name="ID Композиции",
        null=False,
        blank=False,
    )
    rating = models.IntegerField(
        verbose_name="Оценка",
        null=False,
        blank=False,
        default=0,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время",
        null=True
    )

    def __str__(self):
        return f'composition_id = {self.composition_id} - user = {self.user} - rating = {self.rating}'
