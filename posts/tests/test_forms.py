from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Test',
            description='Описание теста',
        )
        cls.group2 = Group.objects.create(
            title='Test2',
            description='Описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.templates = [
            ['index.html', reverse('posts:index')],
            ['post_edit.html',
             reverse('posts:post', kwargs={'username': self.user.username,
                                           'post_id': self.post.id})]
        ]

    def test_post_create(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст поста из формы',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, reverse('posts:index'))
        '''Убедимся, что запись в базе данных не создалась'''
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            group=self.group.id).exists()
        )
        '''Проверка по уникальному id и по автору'''
        self.assertTrue(Post.objects.filter(
            id=self.post.id).filter(author=self.post.author).exists()
        )
        '''Проверка работоспособности'''
        self.assertEqual(response.status_code, 200)

    def test_new_post_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.Field,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_save(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Другой текст!',
            'group': self.group2.id,
        }
        self.authorized_client.post(reverse(
            'posts:post_edit', args=[str(self.post.author), self.post.id]),
            data=form_data, follow=True
        )
        self.assertNotEqual(
            self.post.text, Post.objects.get(id=self.post.id).text,
        )
        self.assertNotEqual(
            self.post.group, Post.objects.get(group=self.group2).group
        )
        self.assertEqual(
            self.post.author, Post.objects.get(author=self.user).author
        )
        self.assertEqual(Post.objects.count(), posts_count,
                         'Количество записей увеличилось')
