from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

INDEX = reverse('posts:index')
NEW_POST = reverse('posts:new_post')


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

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый текст',
            group=self.group
        )
        self.POST_URL = reverse(
            'posts:post',
            args=[self.user.username, self.post.id])
        self.POST_EDIT_URL = reverse(
            'posts:post_edit',
            args=[self.user.username, self.post.id])

    def test_post_create(self):
        post = Post.objects.first()
        post.delete()
        post.save()
        form_data = {
            'text': 'Текст формы',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            NEW_POST,
            data=form_data,
            follow=True
        )
        post = response.context['page'][0]
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group, self.group)
        self.assertRedirects(response, INDEX)

    def test_new_post_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        urls = [
            NEW_POST,
            self.POST_EDIT_URL
        ]
        for url in urls:
            response = self.authorized_client.get(url)
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
        form_data = {
            'text': 'Другой текст!',
            'group': self.group2.id,
        }
        response = self.authorized_client.post(
            self.POST_EDIT_URL,
            data=form_data, follow=True
        )
        '''Пост должен поменяться'''
        post = response.context['post']
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group, self.group2)
        self.assertEqual(post.author, self.post.author)
        self.assertRedirects(response, self.POST_URL)
