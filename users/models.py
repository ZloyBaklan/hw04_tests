from django.db import models
from .validators import validate_not_empty


'''
Визитка, с проверкой на заполненность некоторых полей
'''


class Contact(models.Model):
    name = models.CharField(verbose_name="Ваше имя", max_length=100,
                            validators=[validate_not_empty])
    email = models.EmailField(verbose_name="Ваша почта")
    subject = models.CharField(verbose_name="Тема письма", max_length=100)
    body = models.TextField(verbose_name="Текст письма",
                            validators=[validate_not_empty])
    is_answered = models.BooleanField(default=False)
