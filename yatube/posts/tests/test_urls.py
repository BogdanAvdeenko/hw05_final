from django.test import TestCase, Client
from http import HTTPStatus
from posts.models import Post, Group, User

TEST_FIRST_USERNAME = 'first_test_user'
TEST_SECOND_USERNAME = 'second_test_user'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_POST_TEXT = ('Тестовый пост. Lorem Ipsum. Neque porro quisquam '
                  'est qui dolorem ipsum quia dolor sit amet, consectetur, '
                  'adipisci velit.')
TEST_POST_ID = 1


class StaticURLTests(TestCase):
    def test_homepage(self):
        """Страница / доступна любому пользователю."""
        guest_client = Client()
        response = guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
        )
        cls.post = Post.objects.create(
            author=User.objects.create_user(username=TEST_SECOND_USERNAME),
            text=TEST_POST_TEXT,
        )
        cls.public_urls = {
            '/': 'posts/index.html',
            f'/group/{TEST_GROUP_SLUG}/': 'posts/group_list.html',
            f'/profile/{TEST_FIRST_USERNAME}/': 'posts/profile.html',
            f'/posts/{TEST_POST_ID}/': 'posts/post_detail.html',
        }
        cls.private_urls = {
            '/': 'posts/index.html',
            f'/group/{TEST_GROUP_SLUG}/': 'posts/group_list.html',
            f'/profile/{TEST_FIRST_USERNAME}/': 'posts/profile.html',
            f'/posts/{TEST_POST_ID}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{TEST_POST_ID}/edit/': 'posts/create_post.html',
        }

    def setUp(self):
        # Неавторизованный пользователь
        self.guest_client = Client()
        # Авторизованный пользователь
        self.first_user = User.objects.create_user(
            username=TEST_FIRST_USERNAME
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.first_user)
        # Пользователь - автор поста
        self.second_user = User.objects.get(
            username=TEST_SECOND_USERNAME
        )
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.second_user)

    def test_pages_urls_for_guest_users(self):
        """Тест доступности публичный страниц гостем"""
        for address in PostsURLTests.public_urls:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous_on_auth_login(self):
        """Страница создания поста перенаправит гостя на страницу логина."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_edit_url_redirect_anonymous_on_posts_login(self):
        """Страница редактированния поста перенаправит гостя
        на страницу логина."""
        response = self.guest_client.get(
            f'/posts/{TEST_POST_ID}/edit/', follow=True
        )
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{TEST_POST_ID}/edit/'
        )

    def test_urls_uses_correct_template(self):
        """Соответствие шаблонов для публичных адресов."""
        for address, template in self.public_urls.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_pages_urls_for_auth_users(self):
        """Тест доступности страниц авторизованному пользователю"""
        for address in PostsURLTests.private_urls:
            with self.subTest(address=address):
                response = self.authorized_client_author.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """Соответствие шаблонов для приватных адресов."""
        for address, template in self.private_urls.items():
            with self.subTest(address=address):
                response = self.authorized_client_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_create_url_for_auth_users(self):
        """Страница создания поста доступна авторизованным пользователям"""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_url_redirect_auth_not_author_on_posts_login(self):
        """Страница редактированния поста перенаправит не автора
        на его профайл."""
        response = self.authorized_client.get(
            f'/posts/{TEST_POST_ID}/edit/', follow=True
        )
        self.assertRedirects(response, f'/profile/{TEST_FIRST_USERNAME}/')

    def test_unexisting_page_for_auth_users(self):
        """Страница /unexisting_page/ доступна авторизованным пользователям"""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_unexisting_page_for_guest_users(self):
        """Страница /unexisting_page/ доступна анонимным пользователям"""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
