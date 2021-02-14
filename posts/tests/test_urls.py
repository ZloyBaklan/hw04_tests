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

    def test_urls_status_code(self):
        get_urls_names = [
            [
                INDEX, self.guest_client, 200
            ],
            [
                NEW_POST, self.guest_client, 302
            ],
            [
                GROUP_URL, self.guest_client, 200
            ],
            [
                self.POST_URL, self.guest_client, 200
            ],
            [
                PROFILE_URL, self.guest_client, 200
            ],
            [
                AUTHOR, self.guest_client, 200
            ],
            [
                TECH, self.guest_client, 200
            ],
            [
                self.POST_EDIT_URL, self.guest_client, 302
            ],
            [
                self.POST_EDIT_URL, self.authorized_client, 200
            ],
            [
                NEW_POST, self.authorized_client, 200
            ],
        ]
        for url, client, status in get_urls_names:
            with self.subTest(url=url):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_urls_correct(self):
        urls = [
            [
                NEW_POST,
                self.guest_client.get(NEW_POST, follow=True),
                f'{AUTH_LOGIN}?next={NEW_POST}'
            ],
            [
                self.POST_EDIT_URL,
                self.guest_client.get(self.POST_EDIT_URL, follow=True),
                f'{AUTH_LOGIN}?next={self.POST_EDIT_URL}'
            ],
        ]
        for url, client, redirect in urls:
            with self.subTest(url=url):
                self.assertRedirects(client, redirect)
