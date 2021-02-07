from django.test import TestCase, Client
from posts.models import Group, User, Post


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        '''Делаем запрос к главной странице и проверяем статус'''
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)


class YatubePostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            slug='testgroup',
        )

        cls.post = Post.objects.create(
            id=999,
            text='Тестовый текст',
            author=User.objects.create(username='TestAuthor'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='TestAuthor')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'index.html': '/',
            'new.html': '/new/',
            'group.html': '/group/testgroup/',
            'post.html': '/TestAuthor/999/',
            'profile.html': '/TestAuthor/',
            'author.html': '/about/author/',
            'tech.html': '/about/tech/',
            'new.html': '/TestAuthor/999/edit/',
        }
        for template, url in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_redirect(self):
        response = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')

        if self.user != User.objects.get(username='TestAuthor'):
            response = self.authorized_client.get(
                '/TestAuthor/999/edit/', follow=True
            )
            self.assertRedirects(response, '/TestAuthor/999/')
