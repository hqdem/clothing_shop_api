# Generated by Django 4.1.5 on 2023-01-31 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_contacts',
            field=models.CharField(max_length=127, verbose_name='Контакты пользователя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user_email',
            field=models.EmailField(max_length=254, verbose_name='Email пользователя'),
        ),
    ]
