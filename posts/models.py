from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название группы',
                             null=False)
    slug = models.SlugField(verbose_name='Ссылка', unique=True,
                            help_text='Задайте ссылку на вашу группу')
    description = models.TextField(verbose_name='Описание группы',
                                   max_length=300)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор поста',
                               related_name='posts')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name='Тег группы',
                              related_name='posts', blank=True, null=True,
                              help_text='Ключ для построения ссылки')

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]
