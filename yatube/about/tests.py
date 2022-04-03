from posts.models import User
from django.test import TestCase, Client
from http import HTTPStatus

TEST_USERNAME = 'test_user'


class StaticPagesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urls = [
            '/about/author/',
            '/about/tech/'
        ]

    def setUp(self):
        # Неавторизованного пользователь
        self.guest_client = Client()
        # Авторизованного пользователь
        self.first_user = User.objects.create_user(username=TEST_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.first_user)

    def test_pages_urls_for_guest_users(self):
        """Тест доступности страниц анонимным пользователям"""
        for address in StaticPagesURLTests.urls:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_urls_for_auth_users(self):
        """Тест доступности страниц авторизованному пользователю"""
        for address in StaticPagesURLTests.urls:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
