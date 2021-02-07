from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify
from users.validators import validate_not_empty

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название группы",
                             null=False)
    slug = models.SlugField(verbose_name="Ссылка", unique=True,
                            help_text='Задайте ссылку на вашу группу')
    description = models.TextField(verbose_name="Описание группы",
                                   max_length=300)
    '''
    Расширение встроенного метода save(): если поле slug не заполнено -
    транслитерировать в латиницу содержимое поля title
    '''
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:30]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name="Текст поста",
                            validators=[validate_not_empty])
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="Автор поста",
                               related_name="post_author")
    '''
    Возможность в посте ссылаться на группу.
    Чтобы пост не пропал при удалении группы задаем SET_NULL.
    '''
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              verbose_name="Тег группы",
                              related_name="posts", blank=True, null=True,
                              help_text="Ссылка на группу")

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:15]
