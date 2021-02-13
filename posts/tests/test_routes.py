from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class ReverseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='TestAuthor')
        self.group = Group.objects.create(slug='testgroup',)
        self.post = Post.objects.create(
            text='Тестовый текст',
            author=self.user,
            group=self.group,
        )
        self.urls_names = [
            [
                '/',
                reverse('posts:index')
            ],
            [
                '/about/author/',
                reverse('about:author')
            ],
            [
                '/about/tech/',
                reverse('about:tech')
            ],
            [
                '/new/',
                reverse('posts:new_post')
            ],
            [
                f'/group/{self.group.slug}/',
                reverse('posts:group', args=[self.group.slug])
            ],
            [
                f'/{self.user.username}/',
                reverse('posts:profile', args=[self.user.username])
            ],
            [
                f'/{self.user.username}/{str(self.post.id)}/',
                reverse('posts:post', args=[self.user.username, self.post.id])
            ],
            [
                f'/{self.user.username}/{str(self.post.id)}/edit/',
                reverse('posts:post_edit',
                        args=[self.user.username, self.post.id])
            ]
        ]

    def test_url_uses_correct_reverse(self):
        for direct_url, reversed_url in self.urls_names:
            self.assertEquals(direct_url, reversed_url)
