from django.test import Client, TestCase

from posts.models import Group, Post, User


class YatubePostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='TestAuthor')
        cls.group = Group.objects.create(
            slug='testgroup',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.template_urls_names = [
            ['index.html', '/'],
            ['new.html', '/new/'],
            ['group.html', '/group/' + self.group.slug + '/'],
            ['post.html',
                '/' + self.user.username + '/' + str(self.post.id) + '/'],
            ['profile.html', '/' + self.user.username + '/'],
            ['author.html', '/about/author/'],
            ['tech.html', '/about/tech/'],
            ['new.html', '/' + self.user.username
             + '/' + str(self.post.id) + '/' + 'edit/']
        ]

    def test_urls_uses_correct_template(self):
        for template, url in self.template_urls_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, 200)

    def test_redirect(self):
        response_index = self.guest_client.get('/')
        self.assertEqual(response_index.status_code, 200)
        response_new = self.guest_client.get('/new/', follow=True)
        self.assertRedirects(response_new, '/auth/login/?next=/new/')
        if self.user != User.objects.get(username=self.user.username):
            response = self.authorized_client.get(
                '/' + self.user.username + '/'
                + str(self.post.id) + '/' + 'edit/', follow=True
            )
            self.assertRedirects(
                response, '/' + self.user.username
                + '/' + str(self.post.id) + '/'
            )
