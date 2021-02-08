from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from posts.models import Group, Post, User


class YatubePostsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            author=User.objects.create(username='Тестовый автор'),
            group=Group.objects.create(title='TestG'),
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='Тестовый автор')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    '''Проверка используемых шаблонов'''
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': reverse('posts:index'),
            'group.html': reverse('posts:group',
                                  kwargs={'slug': self.group.slug}),
            'new.html': reverse('posts:new_post'),
            'profile.html': reverse('posts:profile',
                                    kwargs={'username': self.user.username}),
            'post.html': reverse('posts:post',
                                 kwargs={'username': self.user.username,
                                         'post_id': self.post.id}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

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

    def test_index_group_page_show_correct_context(self):
        """Шаблоны index и group сформированы с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:index'))
        post_text_0 = response.context.get('page')[0].text
        post_author_0 = response.context.get('page')[0].author
        post_group_0 = response.context.get('page')[0].group
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_author_0.username, 'Тестовый автор')
        self.assertEqual(post_group_0.title, 'TestG')

        response_group = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': 'TestG'}))
        group_title = response_group.context.get('group').title
        group_slug = response_group.context.get('group').slug
        group_description = response_group.context.get('group').description
        self.assertEqual(group_title, 'Тестовое название группы')
        self.assertEqual(group_slug, 'TestG')
        self.assertEqual(group_description, 'Описание тестовой группы')

    def test_main_page_display_post(self):
        """Пост видно на главной странице"""
        response = self.authorized_client.get(reverse("posts:index"))
        main_page_view = response.context.get("page")
        self.assertIn(self.post, main_page_view)

    def test_profile_page_show_correct_context(self):
        """/<username>/. """
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.user.username})
        )
        post_text_0 = response.context.get('page')[0].text
        post_group_0 = response.context.get('page')[0].group
        post_author_0 = response.context.get('page')[0].author
        post_pub_date_0 = response.context.get('page')[0].pub_date
        author_username_0 = response.context.get('page')[0].author.username
        self.assertEqual(post_text_0, 'Тестовый текст')
        self.assertEqual(post_group_0.title, self.group.slug)
        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_pub_date_0, self.post.pub_date)
        self.assertEqual(author_username_0, self.user.username)


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
                 text=str(i)) for i in range(13)]
        Post.objects.bulk_create(posts)

    def test_first_page_containse_ten_records(self):
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)


class StaticViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.templates_pages_names = {
            'author.html': reverse('about:author'),
            'tech.html': reverse('about:tech')
        }

    def test_author_page_accessible_by_name(self):
        for item in self.templates_pages_names.values():
            with self.subTest():
                response = self.guest_client.get(item)
                self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        for template, reverse_name in self.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
