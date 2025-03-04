# Generated by Django 5.1.6 on 2025-03-04 18:05

import django.contrib.auth.models
import django.utils.timezone
import users.utils
import users.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'password',
                    models.CharField(max_length=128, verbose_name='password'),
                ),
                (
                    'last_login',
                    models.DateTimeField(
                        blank=True, null=True, verbose_name='last login'
                    ),
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='date joined',
                    ),
                ),
                (
                    'email',
                    models.EmailField(
                        max_length=254, unique=True, verbose_name='Email'
                    ),
                ),
                (
                    'username',
                    models.CharField(
                        max_length=150,
                        unique=True,
                        validators=[users.validators.validate_username],
                        verbose_name='Имя пользователя',
                    ),
                ),
                (
                    'first_name',
                    models.CharField(max_length=150, verbose_name='Имя'),
                ),
                (
                    'last_name',
                    models.CharField(max_length=150, verbose_name='Фамилия'),
                ),
                (
                    'avatar',
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=users.utils.get_user_avatar_path,
                        verbose_name='Аватар',
                    ),
                ),
                (
                    'favorite_recipes',
                    models.ManyToManyField(
                        blank=True,
                        related_name='favorite_recipes',
                        to='recipes.recipe',
                    ),
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'shopping_cart',
                    models.ManyToManyField(
                        blank=True,
                        related_name='shopping_cart_recipes',
                        to='recipes.recipe',
                    ),
                ),
                (
                    'subscriptions',
                    models.ManyToManyField(
                        blank=True,
                        related_name='subscribers',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Подписки',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('username',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
