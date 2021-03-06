# Generated by Django 4.0 on 2021-12-15 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_alter_user_wishlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='LetterToSanta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('text', models.TextField(verbose_name='Текст письма')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='letters_to_santa', to='accounts.user')),
            ],
            options={
                'verbose_name': 'Письмо Санте',
                'verbose_name_plural': 'Письма Санте',
            },
        ),
    ]
