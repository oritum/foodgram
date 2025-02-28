"""Утилиты для приложения users."""


def get_user_avatar_path(instance, filename):
    """Генерация пути сохранения аватара."""
    ext = filename.split('.')[-1]
    return f'users/avatars/{instance.username}_avatar.{ext}'
