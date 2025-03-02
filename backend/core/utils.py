"""Утилиты для проекта foodgram_backend."""

from django.conf import settings
from hashids import Hashids


def generate_short_link(
    obj_id: int,
    base_url: str,
    salt: str = settings.SHORTLINK_SALT,
    min_length: int = 3,
) -> str:
    """Генерация короткой ссылки для объекта по ID."""
    hashids = Hashids(salt=salt, min_length=min_length)
    return f'{base_url}s/{hashids.encode(obj_id)}'
