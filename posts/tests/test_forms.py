from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Post, Group, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Test',
            description='Описание теста',
        )
        cls.post = Post.objects.create(
            author=User.objects.create(username='TestAuthor'),
            text='Тестовый текст',
            group=cls.group
        )

    def setUp(self):
        self.user = User.objects.get(username='TestAuthor')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст поста из формы',
            'author': self.user,
            'group': PostFormTests.group.id,
        }

        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(response, '/')
        '''Убедимся, что запись в базе данных не создалась'''
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            group=PostFormTests.group.id).exists()
        )
        '''Проверка работоспособности'''
        self.assertEqual(response.status_code, 200)
    
    def test_post_edit_save(self):
        posts_count = Post.objects.count()
        post = Post.objects.get(id=self.post.id)
        form_data = {
            'text': 'Другой текст!',
            'author': self.user,
            'group': PostFormTests.group.id,
        }
        self.authorized_client.post(
            reverse('posts:post_edit', args=[post.author, post.id]),
            data=form_data,
            follow=True
        )
        self.assertNotEqual(post.text, Post.objects.get(id=self.post.id).text,
                            'Количество записей не изменилось!')
        self.assertEqual(Post.objects.count(), posts_count,
                         'Количество записей увеличилось')
