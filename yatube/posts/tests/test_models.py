from django.test import TestCase
from posts.models import Group, Post, User

TEST_USERNAME = 'test_user'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_POST_TEXT = ('Тестовый пост. Lorem Ipsum. Neque porro quisquam '
                  'est qui dolorem ipsum quia dolor sit amet, consectetur, '
                  'adipisci velit.')


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=TEST_USERNAME)
        cls.group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEST_POST_TEXT,
        )

    def test_model_group_have_correct_object_name(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_model_post_have_correct_object_name(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))

    def test_model_group_have_correct_verbose_name(self):
        """Проверяем, что у модели Group корректно работает verbose_name."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Группа',
            'slug': 'Адрес',
            'description': 'Описание'
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                response = group._meta.get_field(field).verbose_name
                self.assertEqual(response, expected)

    def test_model_post_have_correct_verbose_name(self):
        """Проверяем, что у модели Post корректно работает verbose_name."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                response = post._meta.get_field(field).verbose_name
                self.assertEqual(response, expected)

    def test_model_post_have_correct_help_text(self):
        """Проверяем, что у модели Post корректно работает help_text."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
            'image': 'Загрузите картинку'
        }
        for field, expected in field_help_texts.items():
            with self.subTest(field=field):
                response = post._meta.get_field(field).help_text
                self.assertEqual(response, expected)
