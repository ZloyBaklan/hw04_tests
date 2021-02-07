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

    def setUp(self):
        self.user = User.objects.create_user(username='TestAuthor')
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
