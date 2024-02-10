from django import forms
from books.models import Genres, Composition, Book


class AllInOne(forms.Form):
    """All in one form"""
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}), max_length=100, label='Название книги')
    author = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}), max_length=100, label='Автор')
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}), label='Описание')
    language = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}), max_length=50, label='Язык')
    id_genre = forms.ChoiceField(label='Жанр')
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3'}))
    izdatelstvo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    pages = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3'}))
    coverphoto = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control mb-3'}))
    isbn = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_genre'].choices = [(str(genre.id), genre.name) for genre in Genres.objects.all()]
        