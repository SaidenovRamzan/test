import json
from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from mongoengine import connect, disconnect
from books.models import Genres, Composition, Book


class SearchCompositionApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Подключаемся к тестовой базе данных MongoDB
        disconnect(alias="default")
        cls.db = connect("test_db", host="mongodb://root:example@mongo:27017/")

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api_book_search")

        image_data = Image.new("RGB", (100, 100))
        image_data_io = BytesIO()
        image_data.save(image_data_io, format="JPEG")
        image_data_io.seek(0)
        self.image = SimpleUploadedFile(
            "test.jpg", image_data_io.read(), content_type="image/jpeg"
        )

        self.genre = Genres.objects.create(name="Test Genre")
        self.composition = Composition.objects.create(
            name="Test Composition",
            author="Test Author",
            description="Test Description",
            rent_qte=10,
            language="English",
            id_genre=self.genre,
            is_visible=True,
        )
        self.book = Book.objects.create(
            id_composition=self.composition,
            year=2023,
            izdatelstvo="Test Publishing",
            pages=200,
            coverphoto=self.image,
            isbn="7777777777777",
        )
        self.book_2 = Book.objects.create(
            id_composition=self.composition,
            year=2022,
            izdatelstvo="Test Publishing 2",
            pages=200,
            coverphoto=self.image,
            isbn="7777777777778",
        )
        self.book_3 = Book.objects.create(
            id_composition=self.composition,
            year=2021,
            izdatelstvo="Test Publishing 2",
            pages=200,
            coverphoto=self.image,
            isbn="7777777777779",
        )

    def test_search_book_with_valid_data(self):
        search_request = {"search_request": "Test"}
        response = self.client.post(
            self.url, json.dumps(search_request), content_type="application/json"
        )

        data = json.loads(response.content)

        self.assertEqual(data["books"][0]["name"], "Test Composition")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_publish_houses_by_composition(self):
        url = reverse("api_get_book_publish_houses", kwargs={"pk": self.composition.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        publish_houses = [
            publish_house["publish_house"] for publish_house in data["publish_houses"]
        ]
        expected_publish_houses = ["Test Publishing", "Test Publishing 2"]
        self.assertCountEqual(publish_houses, expected_publish_houses)

    def test_get_publish_houses_by_invalid_composition(self):
        invalid_composition_id = 9999
        url = reverse(
            "api_get_book_publish_houses", kwargs={"pk": invalid_composition_id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_book_years_by_composition(self):
        url = reverse("api_get_book_year", kwargs={"pk": self.composition.pk})
        request = {"izdatelstvo": "Test Publishing 2"}
        response = self.client.post(
            url, json.dumps(request), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        years = [year["year"] for year in data["years"]]
        expected_years = [2022, 2021]
        self.assertCountEqual(years, expected_years)

    def test_get_book_years_by_invalid_composition(self):
        invalid_composition_id = 9999
        url = reverse("api_get_book_year", kwargs={"pk": invalid_composition_id})
        request = {"izdatelstvo": "Test Publishing 2"}
        response = self.client.post(
            url, json.dumps(request), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_book_isbn_by_year(self):
        url = reverse("api_get_isbn", kwargs={"pk": self.composition.pk})
        request = {"izdatelstvo": "Test Publishing 2", "year": 2021}
        response = self.client.post(
            url, json.dumps(request), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        self.assertEqual(data["isbn"], "7777777777779")
        self.assertEqual(data["bookId"], self.book_3.id)

    def test_get_book_isbn_by_invalid_year(self):
        url = reverse("api_get_isbn", kwargs={"pk": self.composition.pk})
        request = {"izdatelstvo": "Test Publishing 2", "year": 2030}
        response = self.client.post(
            url, json.dumps(request), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        if self.composition:
            self.composition.delete()
        if self.genre:
            self.genre.delete()
        for i in Book.objects.all():
            i.delete()
        for i in Composition.objects.all():
            i.delete()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        disconnect(alias="default")
        super().tearDownClass()
