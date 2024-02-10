from django.db import models
from books.models import Book


class UserShelf(models.Model):
    id_book = models.BigIntegerField()
    user = models.ForeignKey(
        'accounts.user',
        on_delete=models.CASCADE,
    )
    count = models.IntegerField()
    price_for_week = models.IntegerField(
        null=True,
        blank=True,
    )
    price_for_sale = models.IntegerField(
        null=True,
        blank=True,
    )

    BOOK_STATE_CHOICES = [
        ('new', 'Новая'),
        ('used', 'Б/У'),
        ('damaged', 'Поврежденная'),
    ]
    book_state = models.CharField(max_length=10, choices=BOOK_STATE_CHOICES)

    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('in_rent', 'В аренде'),
        ('reserved', 'В резерве'),
        ('sold', 'Продана'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    PURPOSE_CHOICES = [
        ('rent', 'В аренду'),
        ('sale', 'На продажу'),
        ('rent and sale', 'В аренду и на продажу'),
    ]
    purpose = models.CharField(max_length=25, choices=PURPOSE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        book_obj = Book.objects.get(pk=self.id_book)       # получаем объект книги
        # и выводим название композиции, а также isbn книги
        return f'Книга: "{book_obj.id_composition.name}" ISBN: {book_obj.isbn}'