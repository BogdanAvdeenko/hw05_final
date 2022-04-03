from posts.models import User
from django.test import TestCase, Client

TEST_USERNAME = 'test_user'


class PageNotFoundTests(TestCase):
    def setUp(self):
        self.first_user = User.objects.create_user(username=TEST_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.first_user)

    def test_urls_uses_correct_template(self):
        """Страница 404 отдает кастомный шаблон"""
        templates_url_names = {
            '/unexpected_page/': 'core/404.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
