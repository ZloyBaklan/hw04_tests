from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User

INDEX = reverse('posts:index')
NEW_POST = reverse('posts:new_post')
AUTHOR = reverse('about:author')
TECH = reverse('about:tech')
USERNAME = 'TestAuthor'
AUTH_LOGIN = reverse('login')
SLUG = 'testgroup'
GROUP_URL = reverse('posts:group', kwargs={'slug': SLUG})
PROFILE_URL = reverse('posts:profile', kwargs={'username': USERNAME})


class YatubePostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=USERNAME)
        cls.group = Group.objects.create(
            slug=SLUG,
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.POST_URL = reverse('posts:post',
                               args=[cls.user.username, cls.post.id])
        cls.POST_EDIT_URL = reverse('posts:post_edit',
                                    args=[cls.user.username, cls.post.id])

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        template_urls_names = [
            ['index.html', INDEX],
            ['new.html', NEW_POST],
            ['group.html', GROUP_URL],
            ['post.html', self.POST_URL],
            ['profile.html', PROFILE_URL],
            ['author.html', AUTHOR],
            ['tech.html', TECH],
            ['new.html', self.POST_EDIT_URL]
        ]
        for template, url in template_urls_names:
            with self.subTest(url=url):
                self.assertTemplateUsed(self.authorized_client.get(url),
                                        template)

    def test_urls_200(self):
        template_urls_names = [
            INDEX,
            NEW_POST,
            GROUP_URL,
            self.POST_URL,
            PROFILE_URL,
            AUTHOR,
            TECH,
            self.POST_EDIT_URL
        ]
        for value in template_urls_names:
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                self.assertEqual(response.status_code, 200)

    def test_redirect_urls_correct(self):
        guest_urls = [
            NEW_POST,
            self.POST_EDIT_URL,
        ]
        for value in guest_urls:
            with self.subTest(value=value):
                response = self.guest_client.get(value, follow=True)
                self.assertRedirects(response, f'{AUTH_LOGIN}?next={value}')
        if self.user != User.objects.get(username=self.user.username):
            response = self.authorized_client.get(
                self.POST_EDIT_URL, follow=True
            )
            self.assertRedirects(response, self.POST_URL)
