from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models


class News(models.Model):
    user = models.ForeignKey(
        verbose_name='Автор',
        to=get_user_model(),
        related_name='news',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        null=False,
        blank=False,
    )
    image = models.ImageField(
        verbose_name='Фото',
        null=False,
        blank=False,
        upload_to='images/news/',
    )
    content = models.TextField(
        verbose_name='Текст контента',
        max_length=20000,
        null=False,
        blank=False,
    )
    is_deleted = models.BooleanField(
        verbose_name='Удалено',
        null=False,
        default=False
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

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            width, height = img.size
            target_ratio = 16 / 9

            # Рассчитываем новые размеры с соотношением 16:9
            if width / height > target_ratio:
                new_width = int(height * target_ratio)
                new_height = height
            else:
                new_width = width
                new_height = int(width / target_ratio)

            # Обрезаем изображение до 16:9 и сохраняем
            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = (width + new_width) / 2
            bottom = (height + new_height) / 2
            img = img.crop((left, top, right, bottom))

            img.thumbnail((1920, 1080))  # Если вы хотите также изменить размер до максимальных 1920x1080
            img.save(self.image.path)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        
    def __str__(self):
        return self.title
