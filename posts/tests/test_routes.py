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
                '/group/' + self.group.slug + '/',
                reverse('posts:group', kwargs={'slug': self.group.slug})
            ],
            [
                '/' + self.user.username + '/',
                reverse('posts:profile', kwargs={'username':
                                                 self.user.username})
            ],
            [
                '/' + self.user.username + '/' + str(self.post.id) + '/',
                reverse('posts:post', kwargs={'username': self.user.username,
                                              'post_id': self.post.id})
            ],
            [
                '/' + self.user.username
                + '/' + str(self.post.id) + '/' + 'edit/',
                reverse('posts:post_edit',
                        kwargs={'username': self.user.username,
                                'post_id': self.post.id})
            ]
        ]

    def test_page_uses_correct_reverse(self):
        for reverse_name in self.templates_pages_names:
            self.assertTemplateUsed(reverse_name)
