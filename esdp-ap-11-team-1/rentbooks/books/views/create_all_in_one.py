from django.views import View
from django.shortcuts import render, redirect

from books.models import Composition, Genres, Book
from books.forms import AllInOne


class AllInOneView(View):
    form = AllInOne

    def get(self, request):
        obj = 0
        form = self.form()
        form.fields["id_genre"].choices = [
            (str(genre.id), genre.name) for genre in Genres.objects.all()
        ]
        return render(request, "book_create.html", context={"forms": form})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        form.fields.get("id_genre").choices = [
            (genre.id, genre.name) for genre in Genres.objects.all()
        ]
        if form.is_valid():
            composition = Composition(
                name=form.cleaned_data["name"],
                author=form.cleaned_data["author"],
                description=form.cleaned_data["description"],
                language=form.cleaned_data["language"],
                id_genre=Genres.objects.get(id=form.cleaned_data["id_genre"]),
            )
            composition.save()
            book = Book(
                id_composition=composition.id_Composition,
                year=form.cleaned_data["year"],
                izdatelstvo=form.cleaned_data["izdatelstvo"],
                pages=form.cleaned_data["pages"],
                coverphoto=form.cleaned_data["coverphoto"],
                isbn=form.cleaned_data["isbn"],
            )
            book.save()
            return render(request, "book_create.html", context={"forms": form})

        return render(request, "book_create.html", context={"forms": form})
