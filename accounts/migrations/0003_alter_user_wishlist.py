# Generated by Django 4.0 on 2021-12-15 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_wishlistitem_alter_user_options_user_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='wishlist',
            field=models.ManyToManyField(blank=True, to='accounts.WishListItem', verbose_name='Пожелания к подарку'),
        ),
    ]
