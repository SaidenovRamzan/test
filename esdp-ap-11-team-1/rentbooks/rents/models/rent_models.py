from django.db import models
import django


class OrderOfRent(models.Model):
    user = models.ForeignKey('accounts.user', on_delete=models.CASCADE)
    usershelf = models.ForeignKey('rents.usershelf', on_delete=models.CASCADE)
    date_create = models.DateTimeField(
        default=django.utils.timezone.now,
    )
    date_plan_start = models.DateField(
        null=True,
        blank=True
    )
    date_plan_end = models.DateField(
        null=True,
        blank=True
    )
    date_fact_start = models.DateField(
        null=True,
        blank=True
    )
    date_fact_end = models.DateField(
        null=True,
        blank=True
    )
    number_for_owner = models.IntegerField(null=True, blank=True)
    number_for_renter = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(
        default=True
    )
    is_approved = models.BooleanField(
        null=True,
        blank=True,
        default=None,
    )
    PURPOSE_CHOICES = [
        ('rent', 'Арендовать'),
        ('buy', 'Купить'),
    ]
    purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default='rent')
    is_finished = models.BooleanField(
        default=False
    )


class UserImages(models.Model):
    book_shelf = models.ForeignKey(
        'rents.usershelf',
        verbose_name='Объявление пользователя',
        related_name='user_images',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    id_book = models.BigIntegerField(
        null=False,
        blank=False,
        default=0
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/book_pics',
        verbose_name='Фото книг',
        default='images/book_pics/blank.jpg'
    )
