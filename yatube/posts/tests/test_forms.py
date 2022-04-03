import shutil
import tempfile

from posts.models import Post, Group, User
from posts.forms import PostForm
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

TEST_USERNAME = 'test_user'
TEST_GROUP_TITLE = 'Тестовая группа'
TEST_GROUP_SLUG = 'test_group_slug'
TEST_GROUP_DESCRIPTION = 'Тестовое описание'
TEST_POST_TEXT = ('Test post. Lorem Ipsum. Neque porro quisquam '
                  'est qui dolorem ipsum quia dolor sit amet, consectetur, '
                  'adipisci velit.')
TEST_CHANGED_POST_TEXT = ('Измененный тестовый пост. Противоположная точка '
                          'зрения подразумевает, что ключевые особенности '
                          'структуры проекта, превозмогая сложившуюся '
                          'непростую экономическую ситуацию, объективно '
                          'рассмотрены соответствующими инстанциями.')
TEST_COMMENT_POST_TEXT = ('Безусловно, высококачественный прототип будущего'
                          'проекта, а также свежий взгляд на привычные'
                          'вещи - безусловно открывает новые горизонты для'
                          'направлений прогрессивного развития!')
TEST_POST_ID = 1


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.forms_user = User.objects.create_user(username=TEST_USERNAME)
        cls.forms_group = Group.objects.create(
            title=TEST_GROUP_TITLE,
            slug=TEST_GROUP_SLUG,
            description=TEST_GROUP_DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.forms_user,
            group=cls.forms_group,
            text=TEST_POST_TEXT,
        )
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username=TEST_USERNAME)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_valid_form_create_post(self):
        """Валидная форма создает запись в базе данных."""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': TEST_POST_TEXT,
            'group': self.forms_group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': TEST_USERNAME})
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text=TEST_POST_TEXT,
                group=self.forms_group.id,
                image='posts/small.gif'
            ).exists()
        )

    def test_valid_form_edit_post(self):
        """Валидная форма post_edit редактирует
        запись в базе данных."""
        posts_count = Post.objects.count()
        form_data = {
            'text': TEST_CHANGED_POST_TEXT,
            'group': self.forms_group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': TEST_POST_ID})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text=TEST_CHANGED_POST_TEXT,
                group=self.forms_group.id
            ).exists()
        )
