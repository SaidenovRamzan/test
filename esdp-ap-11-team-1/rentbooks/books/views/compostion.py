import base64
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from mongoengine.queryset.visitor import Q
import requests

from books.models import (
    Composition,
    Genres,
    Book,
    Comment,
    FavoriteBook,
    Rating,
    FavoriteBook,
)
from books.forms import CompositionForm
from rents.models import UserShelf, OrderOfRent

from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import CompositionTest


class HomeView(View):
    def get(self, request):
        compositions = Composition.objects.all().filter(is_visible=True)
        composition_objects = []
        for composition in compositions:
            if Book.objects.all().filter(id_composition=composition.id):
                coverphoto = (
                    Book.objects.all()
                    .filter(id_composition=composition.id)
                    .first()
                    .coverphoto
                )
                coverphoto = base64.b64encode(coverphoto.read()).decode("utf-8")
            else:
                coverphoto = None

            composition_objects.append(
                {
                    "coverphoto": coverphoto,
                    "book": composition,
                }
            )
        template_name = "index.html"
        context_object_name = "books"
        return render(
            request, template_name, context={context_object_name: composition_objects}
        )


class SearchCompositionView(View):
    model = Composition
    template_name = "books_list.html"

    def get(self, request):
        coverphoto = None
        result = None
        search_value = self.request.GET.get("query")
        if search_value:
            result = self.model.objects.filter(
                Q(name__icontains=search_value)
                | Q(author__icontains=search_value)
                | Q(description__icontains=search_value)
            )
        coverphoto = None
        if result:
            coverphoto = base64.b64encode(
                Book.objects.all()
                .filter(id_composition=result.first().id)
                .first()
                .coverphoto.read()
            ).decode("utf-8")
        return render(
            request,
            self.template_name,
            context={"books": result, "coverphoto": coverphoto},
        )


class ListOfCompositionsView(View):
    model = Composition
    template_name = "list.html"
    paginate_by = 8

    def get(self, request):
        # Парсим query_string
        genre_name = request.GET.get("genre", None)
        purpose = request.GET.get("purpose", None)
        language = request.GET.get("language", None)
        author = request.GET.get("author", None)
        izdatelstvo = request.GET.get("izdatelstvo", None)

        # Достаем все объекты для фильтрации и для проброса в контекст для форм
        genre = Genres.objects.filter(name=genre_name).first()
        compositions = self.model.objects.all()
        languages = self.model.objects.distinct("language")
        authors = self.model.objects.distinct("author")
        izdatelstvos = Book.objects.distinct("izdatelstvo")

        # Производим фильтрацию по данным из query_string
        if genre:
            compositions = compositions.filter(id_genre=genre)
        if purpose:
            user_shelfs = UserShelf.objects.filter(
                purpose__in=[purpose, "rent and sale"]
            )
            book_ids = [user_shelf.id_book for user_shelf in user_shelfs]
            purpose_books = Book.objects.filter(id_Book__in=book_ids)
            purpose_compositions_ids = [
                purpose_book.id_composition.id for purpose_book in purpose_books
            ]
            compositions = compositions.filter(
                id_Composition__in=purpose_compositions_ids
            )
        if language:
            compositions = compositions.filter(language=language)
        if author:
            compositions = compositions.filter(author=author)
        if izdatelstvo:
            books = Book.objects.filter(izdatelstvo=izdatelstvo)
            compositions_ids = [book.id_composition.id for book in books]
            compositions = compositions.filter(id_Composition__in=compositions_ids)

        # Достаем квери сет отфильтрованный по рекамендационным данным
        sorted_compositions = self.sort_by_recommendation_data(compositions)

        # генерируем список объектов composition_objects для проброса картинок в шаблон
        composition_objects = []
        for composition in sorted_compositions:
            if Book.objects.all().filter(id_composition=composition.id):
                coverphoto = base64.b64encode(
                    Book.objects.all()
                    .filter(id_composition=composition.id)
                    .first()
                    .coverphoto.read()
                ).decode("utf-8")
            else:
                coverphoto = None

            composition_objects.append(
                {
                    "coverphoto": coverphoto,
                    "composition": composition,
                }
            )

        # Настройка пагинации
        paginator = Paginator(composition_objects, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # генерируем список объявлений с координатами для карты
        user_shelf_objects = []

        user_shelfs = UserShelf.objects.all()
        for user_shelf in user_shelfs:
            user_shelf_objects.append(
                {
                    "user_shelf": user_shelf,
                    "book": Book.objects.get(id_Book=user_shelf.id_book),
                    "coverphoto": base64.b64encode(
                        Book.objects.get(id_Book=user_shelf.id_book).coverphoto.read()
                    ).decode("utf-8"),
                    "coordinates": list(map(float, self.get_coordinates(user_shelf))),
                }
            )

        return render(
            request,
            self.template_name,
            context={
                "page_obj": page_obj,
                "compositions": composition_objects,
                "ads": user_shelf_objects,
                "genres": Genres.objects.all(),
                "languages": languages,
                "authors": authors,
                "izdatelstvos": izdatelstvos,
                "selected_genre": genre,
                "selected_purpose": purpose,
                "selected_language": language,
                "selected_author": author,
                "selected_izdatelstvo": izdatelstvo,
            },
        )

    def get_coordinates(self, user_shelf):
        base_url = "https://geocode-maps.yandex.ru/1.x/"
        full_address = f"{user_shelf.user.city}, {user_shelf.user.address}"
        params = {
            "apikey": "58e3f0b7-4b3f-4375-afee-1c084e4ef7ea",
            "geocode": full_address,
            "format": "json",
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            response_data = response.json()
            coordinates_str = response_data["response"]["GeoObjectCollection"][
                "featureMember"
            ][0]["GeoObject"]["Point"]["pos"]
            longitude, latitude = coordinates_str.split(" ")
            return latitude, longitude
        else:
            raise Exception(f"Error from Geocoder API: {response.status_code}")

    def sort_by_recommendation_data(self, compositions):
        # Делаем функционал рекомендаций
        user = self.request.user
        if user.id:
            favorites = FavoriteBook.objects.filter(user=user)
        else:
            favorites = []
        if len(favorites) >= 5:
            comp_ids = set(fav.composition_id for fav in favorites)
            comps = Composition.objects.filter(id_Composition__in=comp_ids)
            favorite_genres = set(comp.id_genre for comp in comps)
            favorite_authors = set(comp.author for comp in comps)

            favorite_compositions = compositions.filter(
                id_genre__in=favorite_genres, author__in=favorite_authors
            )
            other_compositions = [
                comp for comp in compositions if comp not in favorite_compositions
            ]
        else:
            favorite_compositions = Composition.objects.none()
            other_compositions = compositions

        ratings = Rating.objects.values("composition_id").annotate(
            avg_rating=Avg("rating")
        )
        for comp in favorite_compositions:
            comp.avg_rating = next(
                (
                    r["avg_rating"]
                    for r in ratings
                    if r["composition_id"] == comp.id_Composition
                ),
                0,
            )
        sorted_favorite_compositions = sorted(
            favorite_compositions,
            key=lambda x: (x.avg_rating, x.rent_qte),
            reverse=True,
        )

        # Сортировка по рейтингу и rent_qte для остальных композиций
        for comp in other_compositions:
            comp.avg_rating = next(
                (
                    r["avg_rating"]
                    for r in ratings
                    if r["composition_id"] == comp.id_Composition
                ),
                0,
            )
        sorted_other_compositions = sorted(
            other_compositions, key=lambda x: (x.avg_rating, x.rent_qte), reverse=True
        )

        # Объединение отсортированных списков
        sorted_compositions = sorted_favorite_compositions + sorted_other_compositions
        return sorted_compositions


class CompositionCreateView(View):
    """Create Composition View"""

    model = Composition
    form = CompositionForm
    template_name = "create_book.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, context={"form": self.form()})

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            for i in range(50_000):
                composition = CompositionTest(
                    name=f"{i}",
                    author=form.cleaned_data["author"],
                    description=form.cleaned_data["description"],
                    rent_qte=form.cleaned_data["rent_qte"],
                    language=form.cleaned_data["language"],
                    id_genre=Genres.objects.get(id=form.cleaned_data["id_genre"]),
                    # is_visible=form.cleaned_data['is_visible']
                )
                composition.save()

            # composition = Composition(
            #     name=form.cleaned_data['name'],
            #     author=form.cleaned_data['author'],
            #     description=form.cleaned_data['description'],
            #     rent_qte=form.cleaned_data['rent_qte'],
            #     language=form.cleaned_data['language'],
            #     id_genre=Genres.objects.get(id=form.cleaned_data['id_genre']),
            #     # is_visible=form.cleaned_data['is_visible']
            # )
            # composition.save()
            return redirect("home")
        return render(
            request,
            self.template_name,
            context={"forms": self.form, "errors": self.form.errors},
        )


class CompositionDetailView(View):
    """Detail Composition view"""

    template_name = "detail_book.html"
    model = Composition

    def get_coordinates(self, user_shelf):
        base_url = "https://geocode-maps.yandex.ru/1.x/"
        full_address = f"{user_shelf.user.city}, {user_shelf.user.address}"
        params = {
            "apikey": "58e3f0b7-4b3f-4375-afee-1c084e4ef7ea",
            "geocode": full_address,
            "format": "json",
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            response_data = response.json()
            coordinates_str = response_data["response"]["GeoObjectCollection"][
                "featureMember"
            ][0]["GeoObject"]["Point"]["pos"]
            longitude, latitude = coordinates_str.split(" ")
            return latitude, longitude
        else:
            raise Exception(f"Error from Geocoder API: {response.status_code}")

    def get(self, request, *args, **kwargs):
        composition = self.model.objects.get(id_Composition=kwargs["pk"])
        # favorites = FavoriteBook.objects.filter(user_id=self.request.user.id, composition_id=kwargs['pk']).exists()
        comments = Comment.objects.filter(composition_id=kwargs["pk"]).order_by(
            "-date_publish"
        )

        books = Book.objects.filter(id_composition=composition.id_Composition)
        # Достаем картинку первой книги, которая привязана к композиции
        try:
            coverphoto_base64 = base64.b64encode(
                books.first().coverphoto.read()
            ).decode("utf-8")
        except:
            coverphoto_base64 = None

        # Достаем все объявления, привязанные к композиции
        user_shelfs = UserShelf.objects.all().filter(
            id_book__in=[id_book.id for id_book in books], is_active=True
        )
        user_shelf_objects = []
        for user_shelf in user_shelfs:
            # Достаем объявление, которое привязано к композиции
            if OrderOfRent.objects.filter(
                user=request.user if request.user.is_authenticated else None,
                usershelf=user_shelf,
                is_active=True,
                is_finished=False,
            ).exists():
                order = OrderOfRent.objects.filter(
                    user=request.user,
                    usershelf=user_shelf,
                    is_active=True,
                    is_finished=False,
                ).first()
            else:
                order = None
            user_shelf_objects.append(
                {
                    "user_shelf": user_shelf,
                    "book": Book.objects.get(id_Book=user_shelf.id_book),
                    "coverphoto": base64.b64encode(
                        Book.objects.get(id_Book=user_shelf.id_book).coverphoto.read()
                    ).decode("utf-8"),
                    "order": order,
                    "coordinates": list(map(float, self.get_coordinates(user_shelf))),
                }
            )
        if self.request.user.id:
            rating_obj = Rating.objects.filter(
                user=self.request.user, composition_id=composition.id_Composition
            ).first()
            rating = rating_obj.rating if rating_obj else 0
        else:
            rating = 0
        avg_rating = Rating.objects.filter(
            composition_id=composition.id_Composition
        ).aggregate(average__rating=Avg("rating"))
        return render(
            request,
            self.template_name,
            context={
                "book": composition,
                # "favorites": favorites,
                "comments": comments,
                "coverphoto_base64": coverphoto_base64,
                "ads": user_shelf_objects,
                "rating": str(rating),
                "avg_rating": avg_rating["average__rating"],
            },
        )


class CompositionUpdateView(View):
    """Updata Composition view"""

    template_name = "update_book.html"
    form_class = CompositionForm
    model = Composition
    success_message = "Данные о книге обновлены!"

    def get(self, request, *args, **kwargs):
        composition = self.model.objects.get(id_Composition=kwargs["pk"])
        return render(
            request,
            self.template_name,
            context={
                "form": self.form_class(
                    {
                        "name": composition.name,
                        "author": composition.author,
                        "description": composition.description,
                        "rent_qte": composition.rent_qte,
                        "id_genre": composition.id_genre.id,
                        "language": composition.language,
                        "is_visible": composition.is_visible,
                    }
                ),
                "book": composition,
            },
        )

    def post(self, request, *args, **kwargs):
        composition = self.model.objects.get(id_Composition=kwargs["pk"])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            composition.name = form.cleaned_data["name"]
            composition.author = form.cleaned_data["author"]
            composition.description = form.cleaned_data["description"]
            composition.rent_qte = form.cleaned_data["rent_qte"]
            composition.language = form.cleaned_data["language"]
            composition.id_genre = Genres.objects.get(id=form.cleaned_data["id_genre"])
            composition.save()
            return redirect("detail_composition", pk=composition.id)
        return render(
            request, self.template_name, context={"forms": form, "errors": form.errors}
        )


class CompositionDeleteView(View):
    template_name = "confirm_delete_book.html"
    model = Composition
    success_url = "home"
    success_message = "Книга удалена!"

    def post(self, request, *args, **kwargs):
        object = self.model.objects.get(id_Composition=kwargs["pk"])
        object.delete()
        return redirect(self.success_url)


class CompositionAdminListView(PermissionRequiredMixin, View):
    permission_required = ("books.view_composition",)

    def get(self, request):
        compositions = Composition.objects.filter(is_visible=False)
        return render(
            request, "admin_compositions.html", context={"compositions": compositions}
        )
