import base64
import logging
import json

from django.db.models import Avg
from mongoengine.queryset.visitor import Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.views import APIView

from api.serializers import FavoriteBookSerializer, CommentSerializer
from books.models import Composition, Genres, Book, Comment, FavoriteBook, Rating

logger = logging.getLogger('main')


class CompositionDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Composition.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))

        # достаем первую книгу, которая связана с данной композицией, чтобы вывести картинку
        response = {
            'id': object.id,
            'name': object.name,
            'author': object.author,
            'genre': Genres.objects.get(id=object.id_genre.id).name,
            'description': object.description,
            'rent_qte': object.rent_qte,
            'coverphoto': base64.b64encode(
                Book.objects.all().filter(id_composition=object.id).first().coverphoto.read()).decode('utf-8'),
        }

        return JsonResponse(response, safe=False, status=status.HTTP_200_OK)


def comment_update_handler(request, pk):
    try:
        comment = get_object_or_404(Comment, id=pk)
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Comment not found'}, status=404)
    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            if 'text' in data:
                comment.text = data['text']
            comment.save()
            return JsonResponse({'id': comment.id, 'text': comment.text}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    if request.method == 'DELETE':
        tempId = comment.pk
        comment.delete()
        return JsonResponse({'id': tempId}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


class AddToFavorites(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        composition_id = request.data.get('composition_id')

        is_favorite = FavoriteBook.objects.filter(user_id=user_id, composition_id=composition_id).exists()

        if is_favorite:
            return JsonResponse({'message': 'Book removed from favorites'}, status=200)
        else:
            FavoriteBook.objects.create(user_id=user_id, composition_id=composition_id)
            return JsonResponse({'message': 'Book added to favorites'}, status=200)


class RemoveFromFavorites(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        book_id = request.data.get('composition_id')
        composition_id = Book.objects.get(id_Book=book_id).id_composition.id
        is_favorite = FavoriteBook.objects.filter(user_id=user_id, composition_id=composition_id).exists()

        if is_favorite:
            FavoriteBook.objects.filter(user_id=user_id, composition_id=composition_id).delete()
            return JsonResponse({'message': 'Book removed from favorites'}, status=200)
        else:
            return JsonResponse({'message': 'Book not found in favorites'}, status=404)


class FavoriteBookViewSet(ModelViewSet):
    serializer_class = FavoriteBookSerializer

    def get_queryset(self):
        user = self.request.user
        return FavoriteBook.objects.filter(user=user)


def search_book_api_view(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            search_request = data.get('search_request', '')

            # Выполняем поиск с использованием Q-объекта
            result = Composition.objects.filter(
                Q(name__icontains=search_request) |
                Q(author__icontains=search_request) |
                Q(description__icontains=search_request)
            )

            compositions = []
            for composition in result:
                book = Book.objects.all().filter(id_composition=composition.id).first()
                compositions.append(
                    {
                        'id': composition.id,
                        'name': composition.name,
                        'author': composition.author,
                        'description': composition.description,
                        'coverphoto': base64.b64encode(book.coverphoto.read()).decode('utf-8'),
                    }
                )

            return JsonResponse({'books': compositions}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


class GetBookPublishHouses(APIView):
    def get_object(self, pk):
        try:
            return Composition.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        object = self.get_object(pk=kwargs.get('pk'))
        books = Book.objects.all().filter(id_composition=object.id_Composition)
        unique_publish_houses = list(set(book.izdatelstvo for book in books))

        # Создаем список словарей
        publish_houses = [{'publish_house': izdatelstvo} for izdatelstvo in unique_publish_houses]
        return JsonResponse({'publish_houses': publish_houses}, status=status.HTTP_200_OK)


class GetBookYearByPublishHouse(APIView):
    def get_object(self, pk):
        try:
            return Composition.objects.get(pk=pk)
        except:
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            izdatelstvo = request.data.get('izdatelstvo', '')
            object = self.get_object(pk=kwargs.get('pk'))
            books = Book.objects.all().filter(id_composition=object.id_Composition).filter(izdatelstvo=izdatelstvo)
            years = [{'year': book.year} for book in books]
            return JsonResponse({'years': years}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


class GetBookISBNByYear(APIView):
    def get_object(self, pk):
        try:
            return Composition.objects.get(pk=pk)
        except:
            raise Http404

    def post(self, request, *args, **kwargs):
        try:
            object = self.get_object(pk=kwargs.get('pk'))
            izdatelstvo = request.data.get('izdatelstvo', '')
            year = int(request.data.get('year', ''))

            book = Book.objects.all().filter(id_composition=object.id_Composition).filter(
                izdatelstvo=izdatelstvo).filter(year=year).first()
            if book:
                return JsonResponse({'isbn': book.isbn, 'bookId': book.id}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


class AddCommentToCompositon(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        composition_id = request.data.get('composition_id')
        text = request.data.get('text')

        comment = Comment.objects.create(user_id=user_id, composition_id=composition_id, text=text)
        return JsonResponse({'id': comment.id, 'text': comment.text}, status=200)


class ListCommentsToCompositon(APIView):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(composition_id=kwargs.get('pk')).order_by('-date_publish')
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)


class AddRatingToCompositon(APIView):
    def post(self, request, *args, **kwargs):
        composition_id = kwargs.get('pk')
        rating = request.data.get('rating')
        user_id = request.data.get('user_id')

        rating_obj, created = Rating.objects.get_or_create(
            user_id=user_id,
            composition_id=composition_id,
            defaults={'rating': rating}
        )
        if not created:
            rating_obj.rating = rating
            rating_obj.save()

        avg_rating = Rating.objects.filter(composition_id=composition_id).aggregate(
            average__rating=Avg('rating'))

        return JsonResponse({
            'success': True,
            'avg_rating': avg_rating,
        }, status=status.HTTP_200_OK)


class CompositionSelectedVisible(APIView):
    def post(self, request, *args, **kwargs):
        compositions = request.data.get('selectedCompositions', [])
        for compostion in compositions:
            composition_id = int(compostion)
            Composition.objects.filter(id_Composition=composition_id).update(is_visible=True)
        return JsonResponse({'data': compositions}, status=status.HTTP_200_OK)


class CompositionAllVisible(APIView):
    def post(self, request, *args, **kwargs):
        compositions = Composition.objects.filter(is_visible=False)
        for composition in compositions:
            composition.is_visible = True
            composition.save()
        return JsonResponse({'data': 'OK'}, status=status.HTTP_200_OK)
