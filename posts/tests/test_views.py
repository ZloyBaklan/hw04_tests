from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import POSTS
from posts.models import Group, Post, User

REVERSE_INDEX = reverse('posts:index')
REVERSE_NEW = reverse('posts:new_post')


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
        cls.reverse_group = reverse('posts:group',
                                    kwargs={'slug': cls.group.slug})
        cls.group_2 = Group.objects.create(
            title="Другая группа",
            slug="group-2",
            description="В этой группе нет постов",
        )
        cls.reverse_group_2 = reverse('posts:group',
                                      kwargs={'slug': cls.group_2.slug})
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.reverse_profile = reverse(
            'posts:profile',
            kwargs={'username': cls.user.username}
        )
        cls.reverse_post = reverse(
            'posts:post',
            kwargs={'username': cls.user.username, 'post_id': cls.post.id}
        )
        cls.reverse_post_edit = reverse(
            'posts:post_edit',
            kwargs={'username': cls.user.username, 'post_id': cls.post.id}
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_group_page_show_correct_context(self):
        """Отображение страницы группы"""
        response_group = self.authorized_client.get(self.reverse_group)
        group_test = response_group.context.get('group')
        self.assertEqual(group_test, self.group)

    def test_post_in_right_group(self):
        """Пост находится в нужной группе"""
        groups_list = {
            'group 2': self.reverse_group_2
        }
        for some_group, reverse_name in groups_list.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                posts_in_group = response.context.get('page')
                if some_group == 'group 2':
                    self.assertNotIn(self.post, posts_in_group)

    def test_main_page_display_post(self):
        """Пост видно на главной странице"""
        response = self.authorized_client.get(REVERSE_INDEX)
        main_page_view = response.context.get("page")
        self.assertIn(self.post, main_page_view)

    def test_profile_page_show_correct_context(self):
        """Корректное отображение контекста на /<username>/ """
        response = self.authorized_client.get(self.reverse_profile)
        post_test = response.context.get('page')[0]
        self.assertEqual(self.post, post_test)

    def test_post_page_show_correct_context(self):
        """Проверка отображения /<username>/<post_id>/. """
        response = self.authorized_client.get(self.reverse_post)
        post_test = response.context.get('post')
        self.assertEqual(post_test, self.post)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        posts = [Post(author=cls.user, text=str(i)) for i in range(POSTS)]
        Post.objects.bulk_create(posts)

    def test_first_page_containse_ten_records(self):
        response = self.client.get(REVERSE_INDEX)
        self.assertEqual(
            len(response.context.get('page').object_list), POSTS
        )

    def test_second_page_containse_three_records(self):
        response = self.client.get(REVERSE_INDEX + '?page=2')
        self.assertEqual(
            len(response.context.get('page').object_list), POSTS
        )
