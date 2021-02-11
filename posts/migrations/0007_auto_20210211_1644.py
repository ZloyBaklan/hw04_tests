# Generated by Django 2.2.6 on 2021-02-11 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20210207_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, help_text='Ключ для построения ссылки', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.Group', verbose_name='Тег группы'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(verbose_name='Текст поста'),
        ),
    ]
