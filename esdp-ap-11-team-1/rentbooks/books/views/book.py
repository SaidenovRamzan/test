from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from books.forms import CompositionForm, BookForm, GenresForm
from books.models import Book, Genres, Composition
from rents.models import UserImages, UserShelf
from api.serializers import UserImagesSerializer
import logging


class AddBookView(View):
    def get(self, request):
        obj = 0
        form = CompositionForm()
        form.fields['id_genre'].choices = [(str(genre.id), genre.name) for genre in Genres.objects.all()]
        logging.info(f"{Composition.objects.all()}==================================")
        logging.info(f"{Book.objects.all()}==================================")
        
        return render(request, 'book__detail.html', context={'forms': form, 'book': obj})

    def post(self, request):
        form = CompositionForm(request.POST)
        form.fields.get('id_genre').choices = [(genre.id, genre.name) for genre in Genres.objects.all()]
        if form.is_valid():
            book = Composition(
                name=form.cleaned_data['name'],
                author=form.cleaned_data['author'],
                description=form.cleaned_data['description'],
                rent_qte=form.cleaned_data['rent_qte'],
                language=form.cleaned_data['language'],
                id_genre=Genres.objects.get(id=form.cleaned_data['id_genre']),
            )
            book.save()
            return render(request, 'book__detail.html',
                          context={'forms': form})  # Перенаправление на страницу успешного добавления книги

        return render(request, 'book__detail.html', context={'forms': form})


class BookView(View):
    def get(self, request):
        form = BookForm()
        form.fields['id_Composition'].choices = [(composition.id, composition.name) for composition in Composition.objects.all()]
        return render(request, 'book_create.html', context={'forms': form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        form.fields.get('id_Composition').choices = [(composition.id, composition.name) for composition in Composition.objects.all()]
        if form.is_valid():
            book = Book(
                id_composition=Composition.objects.get(id_Composition=form.cleaned_data['id_Composition']),
                year=form.cleaned_data['year'],
                izdatelstvo=form.cleaned_data['izdatelstvo'],
                pages=form.cleaned_data['pages'],
                coverphoto=form.cleaned_data['coverphoto'],
                isbn=form.cleaned_data['isbn'],
            )
            book.save()
            return render(request, 'book_create.html', context={'forms': form})
        return render(request, 'book_create.html', context={'forms': form})


class BookCreateView(View):
    model = Book.objects.all()
    form = BookForm()
    template_name = 'create_book.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        self.form.fields['id_Composition'].choices = [(composition.id, composition.name) for composition in Composition.objects.filter(is_visible=True)]
        if not request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, context={'form': self.form})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book(
                id_composition=Composition.objects.get(id_Composition=form.cleaned_data['id_Composition']),
                year=form.cleaned_data['year'],
                izdatelstvo=form.cleaned_data['izdatelstvo'],
                pages=form.cleaned_data['pages'],
                coverphoto=form.cleaned_data['coverphoto'],
                isbn=form.cleaned_data['isbn'],
            )
            book.save()
            return redirect('home')
        return render(request, 'create_book.html', context={'forms': form, 'errors': form.errors})


class BookDetailView(View):
    template_name = 'detail_book.html'
    model = Book

    def get(self, request, *args, **kwargs):
        book = self.model.objects.get(id_Book=kwargs['pk'])
        return render(request, self.template_name, context={'book': book})


class BookUpdateView(View):
    template_name = 'update_book.html'
    form_class = BookForm
    model = Book
    success_message = 'Данные о книге обновлены!'

    def get(self, request, *args, **kwargs):
        book = self.model.objects.get(id_Book=kwargs['pk'])
        # message = f'Пользователь "{self.request.user.username}" обновил информацию о книге "{book.name}" (class BookUpdateView)!'
        # logger.info(message)
        return render(request, self.template_name, context={'form': self.form_class, 'book': book})

    def post(self, request, *args, **kwargs):
        book = self.model.objects.get(id_Book=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            book.id_composition = Composition.objects.get(id_Composition=form.cleaned_data['id_Composition'])
            book.year = form.cleaned_data['year']
            book.izdatelstvo = form.cleaned_data['izdatelstvo']
            book.pages = form.cleaned_data['pages']
            book.coverphoto = form.cleaned_data['coverphoto']
            book.isbn = form.cleaned_data['isbn']
            book.save()
            return redirect('detail_book', pk=book.id)
        return render(request, self.template_name, context={'forms': form, 'errors': form.errors})


class BookDeleteView(View):
    template_name = 'confirm_delete_book.html'
    model = Book
    success_url = 'home'
    success_message = 'Книга удалена!'

    def get(self, request, *args, **kwargs):
        book = self.model.objects.get(id_Book=kwargs['pk'])
        return render(request, self.template_name, context={'book': book})

    def post(self, request, *args, **kwargs):
        object = self.model.objects.get(id_Book=kwargs['pk'])
        object.delete()
        # message = f'Пользователь "{request.user.username}" удалил книгу "{self.object.name}" (class BookDeleteView)!'
        # logger.info(message)
        return redirect(self.success_url)


class AddGenreView(View):
    def get(self, request):
        if request.user.is_staff:
            obj = 0  # Composition.objects.get(id_Book=9)
            form = GenresForm()
            return render(request, 'book__detail.html', context={'forms': form, 'book': obj})
        else:
            return render(request, 'index.html')

    def post(self, request):
        form = GenresForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            genre = Genres(
                name=form.cleaned_data['name'],
            )
            genre.save()
        return render(request, 'book__detail.html',
                          context={'forms': form})  # Перенаправление на страницу успешного добавления книги


class BookDetailImageAPIView(APIView):
    def get_object(self, pk):
        try:
            book = Book.objects.get(pk=pk)
            return book.id_composition
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        rec_image = UserImages.objects.get(id_book=kwargs.get('pk'))
        str_image = str(rec_image.image)
        response = {
            'name': object.name,
            'author': object.author,
            'description': object.description,
            'book_image': str_image
        }

        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)


class BookImageViewSet(viewsets.ModelViewSet):  # добавить
    queryset = UserImages.objects.all()
    serializer_class = UserImagesSerializer

    def list(self, request, *args, **kwargs):
        curr_user = request.user  # получаем текущего пользователя
        ushf_list = []  # создаем пустой список для id объявлений текущего пользователя
        for ushf in UserShelf.objects.all():  # перебираем все объявления
            if ushf.user.id == curr_user.id:  # если объявление принадлежит текущему пользователю,
                ushf_list.append(ushf.id)  # то добавляем id объявления в список

        # фильтруем записи модели UserImages по принадлежности к текущему пользователю
        # В результате, текущий пользователь может видеть и редактировать только свои объявления
        queryset = UserImages.objects.filter(book_shelf_id__in=ushf_list)
        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        id_us = int(request.data['book_shelf'])  # получаем id объявления {'book_shelf': ['3']}
        us = UserShelf.objects.get(pk=id_us)  # получаем объект объявления по id_us
        book_id = us.id_book

        files = request.FILES.getlist('image')  # получаем по ключу image список добавленных объектов картинок
        for file in files:  # перебираем список объектов картинок
            images_data = []
            image_data = {'image': file}
            images_data.append(image_data)  # словарь добавляем в список images_data
            serializer = self.get_serializer(data=images_data,
                                             many=True)  # добавляем список с одним объектом картинки в сериализатор
            serializer.is_valid(raise_exception=True)  # проверка валидности сериализатора
            self.perform_create(serializer, id_us, book_id)  # передаем id объявления (id usershelf) на функцию создания
            headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, id_us, book_id):  # функция создания новой записи с картинкой в UserImages
        serializer.save(id_book=book_id, book_shelf_id=id_us)
