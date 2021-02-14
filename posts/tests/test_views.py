from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import POSTS
from posts.models import Group, Post, User

INDEX = reverse('posts:index')
SLUG = 'TestG'
GROUP = reverse('posts:group', kwargs={'slug': SLUG})
SLUG2 = 'group-2'
GROUP2 = reverse('posts:group', kwargs={'slug': SLUG2})
USERNAME = 'Тестовый автор'
PROFILE = reverse('posts:profile', kwargs={'username': USERNAME})


class YatubePostsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=USERNAME)
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug=SLUG,
            description='Описание тестовой группы',
        )
        cls.group_2 = Group.objects.create(
            title="Другая группа",
            slug=SLUG2,
            description="В этой группе нет постов",
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )
        cls.REVERSE_POST = reverse(
            'posts:post',
            kwargs={'username': cls.user.username, 'post_id': cls.post.id}
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_group_page_show_correct_context(self):
        """Отображение страницы группы"""
        response_group = self.authorized_client.get(GROUP)
        group_test = response_group.context.get('group')
        self.assertEqual(group_test, self.group)

    def test_post_in_url(self):
        urls_names = [
            GROUP,
            INDEX,
            PROFILE,
        ]
        for value in urls_names:
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                self.assertEqual(self.post.id, 
                                 response.context.get('page')[0].id)
                self.assertEqual(self.post.author, 
                                 response.context.get('page')[0].author)

    def test_post_not_in_group2(self):
        """Пост не отображается в другой группе"""
        response_group = self.authorized_client.get(GROUP2)
        posts_in_group = response_group.context.get('page')
        self.assertNotIn(self.post, posts_in_group)

    def test_post_page_show_correct_context(self):
        """Проверка отображения /<username>/<post_id>/. """
        response = self.authorized_client.get(self.REVERSE_POST)
        self.assertEqual(self.post, response.context.get('post'))
        self.assertEqual(self.post.author, response.context.get('post').author)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='test_user')
        posts = [Post(author=cls.user, text=str(i)) for i in range(POSTS)]
        Post.objects.bulk_create(posts)

    def test_page_count_records(self):
        response = self.client.get(INDEX)
        self.assertEqual(
            len(response.context.get('page').object_list), POSTS
        )
