from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from mongoengine import connect, disconnect

from books.models import Genres, Composition, Book


class CompositionCreationTest(TestCase):
    count = 0

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        disconnect(alias="default")  # Разрыв текущего соединения
        cls.db = connect(
            db="test_db", host="mongo", username="root", password="example"
        )

    def setUp(self):
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

    # Тестирование создания и чтение композиции
    def test_name_creation(self):
        composition = Composition.objects.first()
        self.assertEqual(composition.name, "Test Composition")

    def test_author_creation(self):
        composition = Composition.objects.first()
        self.assertEqual(composition.author, "Test Author")

    def test_description_creation(self):
        composition = Composition.objects.first()
        self.assertEqual(composition.description, "Test Description")

    def test_rent_qte_creation(self):
        composition = Composition.objects.first()
        self.assertEqual(composition.rent_qte, 10)

    def test_language_creation(self):
        composition = Composition.objects.first()
        self.assertEqual(composition.language, "English")

    def test_id_genre_creation(self):
        genre = Genres.objects.first()
        self.assertEqual(genre.name, "Test Genre")

    def test_is_visible_creation(self):
        composition = Composition.objects.first()
        self.assertEqual(composition.is_visible, True)

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
        # Отключаемся от тестовой базы данных при завершении всех тестов
        cls.db.close()
        disconnect(alias="default")
        super().tearDownClass()


class BookCreationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Подключаемся к тестовой базе данных MongoDB
        disconnect(alias="default")
        cls.db = connect(
            db="test_db", host="mongo", username="root", password="example"
        )

    def setUp(self):
        self.genre = Genres.objects.create(name="Test Genre")
        self.composition = Composition.objects.create(
            name="Чебурашка",
            author="Test Author",
            description="Test Description",
            rent_qte=10,
            language="English",
            id_genre=self.genre,
            is_visible=True,
        )

        image_data = Image.new("RGB", (100, 100))
        image_data_io = BytesIO()
        image_data.save(image_data_io, format="JPEG")
        image_data_io.seek(0)
        self.image = SimpleUploadedFile(
            "test.jpg", image_data_io.read(), content_type="image/jpeg"
        )

        self.book = Book.objects.create(
            id_composition=self.composition,
            year=1999,
            izdatelstvo="Просвещение",
            pages=200,
            isbn="123321",
            coverphoto=self.image,
        )

    # Тестирование создания и чтение книги
    def test_name_creation(self):
        composition = Composition.objects.filter(name="Чебурашка").first()
        self.assertEqual(composition.name, "Чебурашка")

    def test_year_creation(self):
        book = Book.objects.first()
        self.assertEqual(book.year, 1999)

    def test_izdatelstvo_creation(self):
        book = Book.objects.first()
        self.assertEqual(book.izdatelstvo, "Просвещение")

    def test_pages_creation(self):
        book = Book.objects.first()
        self.assertEqual(book.pages, 200)

    def test_isbn_creation(self):
        book = Book.objects.first()
        self.assertEqual(book.isbn, "123321")

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
        # Отключаемся от тестовой базы данных при завершении всех тестов
        cls.db.close()
        disconnect(alias="default")
        super().tearDownClass()
