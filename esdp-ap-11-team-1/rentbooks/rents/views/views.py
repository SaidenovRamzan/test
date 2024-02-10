import base64
import requests
from django.views.generic import DetailView

from books.models import Book
from rents.models import UserShelf
from rents.models import UserImages


class UserShelfDetailView(DetailView):
    model = UserShelf
    template_name = 'user_shelf_detail.html'
    context_object_name = 'user_shelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(id_Book=self.object.id_book)
        context['name'] = book.id_composition.name
        context['coverphoto'] = base64.b64encode(book.coverphoto.read()).decode('utf-8')
        context['user_images'] = self.get_user_images()
        context['izdatelstvo'] = book.izdatelstvo
        context['isbn'] = book.isbn
        context['coordinates'] = list(map(float, self.get_coordinates()))
        return context

    def get_user_images(self):
        images = UserImages.objects.filter(book_shelf=self.object)
        url_images = [image.image.url for image in images]
        return url_images

    def get_coordinates(self):
        base_url = "https://geocode-maps.yandex.ru/1.x/"
        full_address = f"{self.object.user.city}, {self.object.user.address}"
        params = {
            "apikey": '58e3f0b7-4b3f-4375-afee-1c084e4ef7ea',
            "geocode": full_address,
            "format": "json"
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            response_data = response.json()
            coordinates_str = \
            response_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            longitude, latitude = coordinates_str.split(' ')
            return latitude, longitude
        else:
            raise Exception(f"Error from Geocoder API: {response.status_code}")