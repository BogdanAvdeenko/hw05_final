from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group, User
from posts.forms import PostForm

TEST_USERNAME = 'test_user'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_POST_TEXT = ('Тестовый пост. Lorem Ipsum. Neque porro quisquam '
                  'est qui dolorem ipsum quia dolor sit amet, consectetur, '
                  'adipisci velit.')
TEST_POST_ID = 1
TEST_PAGINATOR_FIRST_PAGE = 10
TEST_PAGINATOR_SECOND_PAGE = 4


def get_field_from_context(context, field_type):
    """Получить поле из контекста."""
    for field in context.keys():
        if field not in ('user', 'request') and isinstance(
            context[field], field_type
        ):
            return context[field]
    return


class PostsPagesTests(TestCase):
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
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text=TEST_POST_TEXT,
        )
        cls.templates_for_auth_users = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group', kwargs={'slug': TEST_GROUP_SLUG}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': TEST_USERNAME}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': TEST_POST_ID}
            ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': TEST_POST_ID}
            ): 'posts/create_post.html',
        }
        cls.templates_for_all_users = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group', kwargs={'slug': TEST_GROUP_SLUG}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': TEST_USERNAME}
            ): 'posts/profile.html',
        }

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(
            username=TEST_USERNAME
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """Views - URL-адрес использует соответствующий шаблон."""
        for reverse_name, template in self.templates_for_auth_users.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_group_list_profile_pages_show_correct_context(self):
        """Шаблоны index, group_list, profile
        сформированы с правильным контекстом."""
        for reverse_name in self.templates_for_all_users:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                post_on_correct_page = response.context.get('page_obj')[0]
                self.assertEqual(post_on_correct_page.text, self.post.text)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        post_context = get_field_from_context(response.context, Post)
        assert post_context is not None, (
            'Шаблон post_detail сформирован с неправильным контекстом'
        )

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create'))
        postform_context = get_field_from_context(response.context, PostForm)
        assert postform_context is not None, (
            'Шаблон post_create сформирован с неправильным контекстом'
        )

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}))
        post_context = get_field_from_context(response.context, Post)
        postform_context = get_field_from_context(response.context, PostForm)
        assert any([post_context, postform_context]) is not None, (
            'Шаблон post_edit сформирован с неправильным контекстом'
        )


class PaginatorViewsTest(TestCase):
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
        for i in range(14):
            cls.post = Post.objects.create(
                author=cls.user,
                group=cls.group,
                text=TEST_POST_TEXT,
            )
        cls.templates_for_all_users = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group', kwargs={'slug': TEST_GROUP_SLUG}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': TEST_USERNAME}
            ): 'posts/profile.html',
        }

    def setUp(self):
        self.user = User.objects.get(
            username=TEST_USERNAME
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """Проверка паджинатора: на первой странице должно быть 10 постов."""
        for reverse_name in self.templates_for_all_users:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(len(
                    response.context['page_obj']), TEST_PAGINATOR_FIRST_PAGE
                )

    def test_second_page_contains_three_records(self):
        """Проверка паджинатора: на второй странице должно быть 4 поста."""
        for reverse_name in self.templates_for_all_users:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name + '?page=2')
                self.assertEqual(len(
                    response.context['page_obj']), TEST_PAGINATOR_SECOND_PAGE
                )
