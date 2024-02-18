from django.test import TestCase
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from news.models import News
from django.core.exceptions import ValidationError
import logging


class NewsModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="testuser", password="testpassword", age=20, phone="+7 708 1636294"
        )

    def setUp(self):
        # Создаем изображение для тестирования
        image_data = Image.new("RGB", (100, 100))
        image_data_io = BytesIO()
        image_data.save(image_data_io, format="JPEG")
        image_data_io.seek(0)
        self.image = SimpleUploadedFile(
            "test.jpg", image_data_io.read(), content_type="image/jpeg"
        )

    # Тесты на корректное создание новостей
    def test_news_creation(self):
        news = self.create_news()
        self.assertEqual(news.user, self.user),
        self.assertEqual(news.title, "Test news title"),
        self.assertEqual(news.content, "test content for news")
        self.assertFalse(news.is_deleted)

        self.assertTrue(news.image.name.startswith("images/news/"))

    def test_invalid_title_news_creation(self):
        with self.assertRaises(ValidationError):
            news = News(
                user=self.user,
                title="",
                image=self.image,
                content="test content for news",
            )
            news.full_clean()

    def test_invalid_image_news_creation(self):
        with self.assertRaises(ValidationError):
            news = News.objects.create(
                user=self.user,
                title="Test news title",
                image=None,
                content="test content for news",
            )
            news.full_clean()

    def test_invalid_content_news_creation(self):
        with self.assertRaises(ValidationError):
            news = News.objects.create(
                user=self.user,
                title="Test news title",
                image=self.image,
                content="",
            )
            news.full_clean()

    def test_news_creation_without_user(self):
        news = News.objects.create(
            user=None,
            title="Test news title",
            image=self.image,
            content="test content for news",
        )
        self.assertIsNone(news.user)

    # Тесты на обновление данных новости
    def test_update_news_title(self):
        news = self.create_news()
        self.assertTrue(News.objects.filter(id=news.id).exists())

        new_title = "New test title"
        news.title = new_title
        news.save()
        self.assertEqual(News.objects.get(id=news.id).title, new_title)

    def test_update_news_image(self):
        news = self.create_news()
        self.assertTrue(News.objects.filter(id=news.id).exists())

        new_image_data = Image.new("RGB", (200, 200))
        new_image_data_io = BytesIO()
        new_image_data.save(new_image_data_io, format="JPEG")
        new_image_data_io.seek(0)
        new_image = SimpleUploadedFile(
            "test2.jpg", new_image_data_io.read(), content_type="image/jpeg"
        )
        news.image = new_image
        news.save()

        self.assertTrue(
            News.objects.get(id=news.id).image.name.startswith("images/news/")
        )

    def test_update_news_content(self):
        news = self.create_news()
        self.assertTrue(News.objects.filter(id=news.id).exists())

        new_content = (
            "Tenetur quod quidem in voluptatem corporis dolorum dicta sit pariatur porro quaerat"
            " autem ipsam odit quam beatae tempora quibusdam illum! Modi velit odio nam nulla "
            "unde amet odit pariatur at! Tenetur quod quidem in voluptatem corporis dolorum dicta"
            " sit pariatur porro quaerat autem ipsam odit quam beatae tempora quibusdam illum!"
            " Modi velit odio nam nulla unde amet odit pariatur at! Tenetur quod quidem in voluptatem"
            " corporis dolorum dicta sit pariatur porro quaerat autem ipsam odit quam beatae tempora"
            " quibusdam illum! Modi velit odio nam nulla unde amet odit pariatur at!"
        )
        news.content = new_content
        news.save()

        self.assertEqual(News.objects.get(id=news.id).content, new_content)

    # Тест на удаление новости
    def test_news_deletion(self):

        news = self.create_news()
        self.assertTrue(News.objects.filter(id=news.id).exists())

        news.delete()
        self.assertTrue(news.is_deleted)

    def create_news(self):
        news = News.objects.create(
            user=self.user,
            title="Test news title",
            image=self.image,
            content="test content for news",
        )

        return news

    def tearDown(self):
        self.image.close()
