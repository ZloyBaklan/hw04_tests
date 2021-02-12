from django.test import Client, TestCase

from posts.models import Group, Post, User

URL_INDEX = '/'
URL_NEW = '/new/'
URL_AUTHOR = '/about/author/'
URL_TECH = '/about/tech/'


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
        cls.slug_group = '/group/' + cls.group.slug + '/'
        cls.slug_profile = '/' + cls.user.username + '/'
        cls.slug_post = ('/' + cls.user.username
                         + '/' + str(cls.post.id) + '/')
        cls.slug_post_edit = ('/' + cls.user.username
                              + '/' + str(cls.post.id) + '/' + 'edit/')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        template_urls_names = [
            ['index.html', URL_INDEX],
            ['new.html', URL_NEW],
            ['group.html', self.slug_group],
            ['post.html', self.slug_post],
            ['profile.html', self.slug_profile],
            ['author.html', URL_AUTHOR],
            ['tech.html', URL_TECH],
            ['new.html', self.slug_post_edit]
        ]
        for template, url in template_urls_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
                self.assertEqual(response.status_code, 200)

    def test_redirect(self):
        response_index = self.guest_client.get(URL_INDEX)
        self.assertEqual(response_index.status_code, 200)
        response_new = self.guest_client.get(URL_NEW, follow=True)
        self.assertRedirects(response_new, '/auth/login/?next=' + URL_NEW)
        if self.user != User.objects.get(username=self.user.username):
            response = self.authorized_client.get(
                self.slug_post_edit, follow=True
            )
            self.assertRedirects(response, self.slug_post)
