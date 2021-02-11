from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class SlugTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='TestAuthor')
        self.group = Group.objects.create(slug='testgroup',)
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group,
        )
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        '''Проверка используемых шаблонов'''
        self.templates_pages_names = [
            ['index.html', reverse('posts:index')],
            ['author.html', reverse('about:author')],
            ['tech.html', reverse('about:tech')],
            ['group.html', reverse(
                'posts:group', kwargs={'slug': self.group.slug}
            )],
            ['profile.html', reverse(
                'posts:profile', kwargs={'username': self.user.username}
            )],
            ['post.html', reverse('posts:post',
                                  kwargs={'username': self.user.username,
                                          'post_id': self.post.id})],
        ]

    def test_page_uses_correct_template(self):
        for template, reverse_name in self.templates_pages_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, 200)
