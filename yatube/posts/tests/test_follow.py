from django.test import Client, TestCase
from django.urls import reverse
from posts.models import User, Follow, Post


TEST_USERNAME = 'test_user'
TEST_AUTHOR_USERNAME = 'test_user_author'
TEST_AUTHOR_FOLLOWING = 'test_following_author'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_POST_TEXT = ('Тестовый пост. Lorem Ipsum. Neque porro quisquam '
                  'est qui dolorem ipsum quia dolor sit amet, consectetur, '
                  'adipisci velit.')


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.author = User.objects.create_user(username=TEST_AUTHOR_USERNAME)
        cls.following_author = User.objects.create_user(
            username=TEST_AUTHOR_FOLLOWING
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text=TEST_POST_TEXT,
        )

        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.following_author,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_following_client = Client()
        self.authorized_following_client.force_login(self.following_author)

    def test_create_follow(self):
        """Проверка подписки"""
        follow_count = Follow.objects.count()
        response = self.authorized_client.post(
            reverse('posts:profile_follow', args=[self.author]),
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            args=[self.author])
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user,
                author=self.author
            ).exists()
        )
        # Подписчик видит пост автора
        subscriber = self.authorized_client.get(reverse('posts:follow_index'))
        subscriber_can_see_post = subscriber.context.get('page_obj')[0]
        self.assertEqual(self.post.text, subscriber_can_see_post.text)
        # Не подписанный не видит пост автора
        unsubscriber = self.authorized_following_client.get(
            reverse('posts:follow_index')
        )
        subscriber_can_see_post = unsubscriber.context.get('page_obj')
        self.assertNotEqual(self.post, subscriber_can_see_post)

    def test_unfollow(self):
        """Проверка отписки"""
        follow_count = Follow.objects.count()
        response = self.authorized_client.post(
            reverse('posts:profile_unfollow', args=[self.following_author]),
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            args=[self.following_author])
        )
        self.assertEqual(Follow.objects.count(), follow_count - 1)
