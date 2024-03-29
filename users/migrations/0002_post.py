# Generated by Django 3.1.5 on 2021-01-22 08:29

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(blank=True, max_length=200, null=True)),
                ('text', models.TextField(validators=[users.validators.validate_not_empty])),
            ],
        ),
    ]
