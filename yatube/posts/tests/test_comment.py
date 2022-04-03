from django.test import TestCase, Client
from http import HTTPStatus
from posts.models import Post, Group, User
from django.urls import reverse
from posts.forms import CommentForm

TEST_USERNAME = 'test_user'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_COMMENT_POST_TEXT = 'Тестовый пост'
TEST_POST_ID = 1


class CommentsTests(TestCase):
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
            author=User.objects.create_user(username=TEST_USERNAME),
            text=TEST_COMMENT_POST_TEXT,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username=TEST_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_comment_url_redirect_anonymous_on_posts_login(self):
        """Страница комментирования поста перенаправит гостя
        на страницу логина."""
        response = self.guest_client.get(
            f'/posts/{TEST_POST_ID}/comment/', follow=True
        )
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{TEST_POST_ID}/comment/'
        )

    def test_valid_form_add_comment(self):
        """После успешной отправки комментарий
        появляется на странице поста."""
        form = CommentForm(data={
            'text': TEST_COMMENT_POST_TEXT,
        })
        self.assertTrue(form.is_valid())
        response = self.authorized_client.post(
            reverse('posts:add_comment', args=[self.post.pk]),
            data=form.data,
            follow=True
        )
        # Проверяем наличие комментария
        self.assertEqual(self.post.comments.last().text, form.data['text'])
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            args=[self.post.pk])
        )
