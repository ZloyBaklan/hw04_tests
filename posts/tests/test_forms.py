from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

REVERSE_INDEX = reverse('posts:index')
REVERSE_NEW_POST = reverse('posts:new_post')


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestsAuthor')
        cls.group = Group.objects.create(
            title='Test',
            slug='Tests',
            description='Описание теста',
        )
        cls.group2 = Group.objects.create(
            title='Test2',
            slug='Tests2',
            description='Описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group
        )
        cls.reverse_post_edit = reverse('posts:post',
                                        kwargs={'username': cls.user.username,
                                                'post_id': cls.post.id})

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        form_data = {
            'text': 'Текст поста из формы',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            REVERSE_NEW_POST,
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, REVERSE_INDEX)
        '''Проверка по автору(автор не может быть изменен)'''
        self.assertTrue(Post.objects.filter(author=self.post.author).exists())
        '''Проверка работоспособности'''
        self.assertEqual(response.status_code, 200)

    def test_new_post_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(REVERSE_NEW_POST
                                              or self.reverse_post_edit)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.Field,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        """Корректное отображение /<username>/<post_id>/edit/. """

    def test_post_edit_save(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Другой текст!',
            'group': self.group2.id,
        }
        self.authorized_client.post(
            self.reverse_post_edit,
            data=form_data, follow=True
        )
        '''id поста автора не должен поменяться'''
        self.assertEqual(
            self.post.id, Post.objects.get(author=self.post.author).id,
        )
        self.assertEqual(Post.objects.count(), posts_count)
