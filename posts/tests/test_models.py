from django.test import TestCase

from posts.models import Group, Post, User


class YatubePostsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        '''Создание тестовых записей в БД'''
        cls.user = User.objects.create(username='Тестовый автор')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='Тестовая ссылка группы',
            description='Описание тестовой группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = YatubePostsTest.post
        field_verboses = {
            'text': 'Текст поста',
            'author': 'Автор поста',
            'group': 'Тег группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)
        group = YatubePostsTest.group
        field_verboses = {
            'title': 'Название группы',
            'slug': 'Ссылка',
            'description': 'Описание группы',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = YatubePostsTest.post
        field_help_texts = {
            'group': 'Ключ для построения ссылки'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)
        group = YatubePostsTest.group
        field_help_texts = {
            'slug': 'Задайте ссылку на вашу группу'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_object_name_is_title_field(self):
        '''__str__  group - строка с group.title.'''
        group = YatubePostsTest.group
        expected_object_name = group.title
        self.assertEquals(expected_object_name, str(group))

    def test_object_name_is_text_field(self):
        '''__str__  post - строка с post.text.'''
        post = YatubePostsTest.post
        expected_object_name = post.text
        self.assertEquals(expected_object_name, str(post))
