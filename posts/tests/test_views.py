from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import postsconstant
from posts.models import Group, Post, User


class YatubePostsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Тестовый автор')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='TestG',
            description='Описание тестовой группы',
        )
        cls.group_2 = Group.objects.create(
            title="Другая группа",
            slug="group-2",
            description="В этой группе нет постов",
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.template_pages_names = [
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

    def test_group_page_show_correct_context(self):
        """Отображение страницы группы"""
        response_group = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': self.group.slug}))
        group_test = response_group.context.get('group')
        self.assertEqual(group_test, self.group)

    def test_post_in_right_group(self):
        """Пост находится в нужной группе"""
        groups_list = {
            'group 1': reverse('posts:group', args=[self.group.slug]),
            'group 2': reverse('posts:group', args=[self.group_2.slug])
        }
        for some_group, reverse_name in groups_list.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                posts_in_group = response.context.get('page')
                if some_group == 'group 1':
                    self.assertIn(self.post, posts_in_group)
                else:
                    self.assertNotIn(self.post, posts_in_group)

    def test_main_page_display_post(self):
        """Пост видно на главной странице"""
        response = self.authorized_client.get(reverse("posts:index"))
        main_page_view = response.context.get("page")
        self.assertIn(self.post, main_page_view)

    def test_profile_page_show_correct_context(self):
        """Корректное отображение контекста на /<username>/ """
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username})
        )
        post_test = response.context.get('page')[0]
        self.assertEqual(self.post, post_test)

    def test_post_page_show_correct_context(self):
        """Проверка отображения /<username>/<post_id>/. """
        response = self.authorized_client.get(reverse(
            'posts:post',
            kwargs={'username': self.user.username, 'post_id': self.post.id})
        )
        post_test = response.context.get('post_V')[0]
        self.assertEqual(post_test, self.post)

    def test_post_edit_page_show_correct_context(self):
        """Корректное отображение /<username>/<post_id>/edit/. """
        response = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'username': self.user.username, 'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        field_not_empty = response.context.get('post')
        self.assertEqual(field_not_empty, self.post)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        cls.group = Group.objects.create(
            title='TestGroup',
            description='Тестовое описание'
        )
        posts = [Post(author=cls.user, group=cls.group,
                 text=str(i)) for i in range(postsconstant + 3)]
        Post.objects.bulk_create(posts)

    def test_first_page_containse_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(
            len(response.context.get('page').object_list), postsconstant
        )

    def test_second_page_containse_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(
            len(response.context.get('page').object_list), postsconstant - 7
        )
