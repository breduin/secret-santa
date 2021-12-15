# Generated by Django 4.0 on 2021-12-15 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите пожелание', max_length=256, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Элемент списка пожеланий',
                'verbose_name_plural': 'Элементы списка пожеланий',
            },
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Почтовый адрес'),
        ),
        migrations.AddField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.WishListItem', verbose_name='Пожелания к подарку'),
        ),
    ]
