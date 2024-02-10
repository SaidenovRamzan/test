from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class LoginViewTest(TestCase):
    def setUp(self):
        self.username = 'ramzan'
        self.password = '2412'
        self.user = get_user_model().objects.create_user(
            username='ramzan',
            password='2412',
            age=20,
            phone='+7 708 1636294'
        )
        self.login_url = reverse('login')

    def test_login(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)  # Проверьте, что успешно вошли
        self.assertRedirects(response,
                             reverse('user_profile'))  # Проверьте, что после входа перенаправляет на домашнюю страницу

    def test_login_failure(self):
        response = self.client.post(self.login_url, {'username': self.username, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 200)  # Проверьте, что не удалось войти
        self.assertContains(response,
                            "Please enter a correct username and password.")  # Проверьте наличие сообщения об ошибке входа