from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import (
    EMAIL_MAX_LENGTH,
    FIRST_NAME_MAX_LENGTH,
    LAST_NAME_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_PREVIEW_MAX_LENGTH,
)
from users.utils import get_user_avatar_path
from users.validators import validate_username


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Email',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[validate_username],
    )
    first_name = models.CharField(
        'Имя',
        max_length=FIRST_NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LAST_NAME_MAX_LENGTH,
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to=get_user_avatar_path,
        null=True,
        blank=True,
    )
    subscriptions = models.ManyToManyField(
        'self',
        verbose_name='Подписки',
        related_name='subscribers',
        symmetrical=False,
        blank=True,
    )
    favorite_recipes = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorite_recipes',
        blank=True,
    )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='shopping_cart_recipes',
        blank=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:USERNAME_PREVIEW_MAX_LENGTH]
