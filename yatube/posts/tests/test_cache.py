from posts.models import Post, Group, User
from django.test import TestCase, Client
from django.test import Client, TestCase
from django.urls import reverse
from django.core.cache import cache


TEST_USERNAME = 'test_user'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_POST_TEXT = ('Тестовый пост. Lorem Ipsum. Neque porro quisquam '
                  'est qui dolorem ipsum quia dolor sit amet, consectetur, '
                  'adipisci velit.')
TEST_POST_ID = 1


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username=TEST_USERNAME
        )
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(
            username=TEST_USERNAME
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_cache(self):
        """Тестирование кэша"""
        new_post = Post.objects.create(
            author=self.user,
            text=TEST_POST_TEXT,
            group=self.group,
        )
        response = self.authorized_client.get(
            reverse('posts:index')
        ).content
        new_post.delete()
        response_cach = self.authorized_client.get(
            reverse('posts:index')
        ).content
        self.assertEqual(response, response_cach)
        cache.clear()
        response_clear_cach = self.authorized_client.get(
            reverse('posts:index')
        ).content
        self.assertNotEqual(response, response_clear_cach)
