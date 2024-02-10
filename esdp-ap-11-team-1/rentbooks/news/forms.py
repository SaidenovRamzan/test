from django import forms
from django.core.validators import MinLengthValidator
from django.forms import Textarea

from news.models import News


class NewsForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(
                limit_value=10,
                message='Минимальная длина заголовка - 10!',
            )
        ],
    )
    content = forms.CharField(
        max_length=20000,
        validators=[
            MinLengthValidator(
                limit_value=100,
                message='Минимальная длина текста - 100!',
            )
        ],
        widget=Textarea,
        label='Текст новости',
    )

    class Meta:
        model = News
        fields = ('title', 'image', 'content')
        labels = {
            'title': 'Заголовок новости',
            'image': 'Вставьте картинку горизонтального формата',
            'content': 'Текст новости',
        }
