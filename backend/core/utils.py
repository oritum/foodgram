"""Утилиты для проекта foodgram_backend."""

from django.conf import settings
from drf_extra_fields.fields import Base64ImageField
from hashids import Hashids


class Base64ImageField(Base64ImageField):
    """Поле для работы с изображениями в формате base64 с абсолютным URL."""

    def to_representation(self, value):
        if not value:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(value.url)
        return value.url


def generate_short_link(
    obj_id: int,
    base_url: str,
    salt: str = settings.SHORTLINK_SALT,
    min_length: int = 3,
) -> str:
    """Генерация короткой ссылки для объекта по ID."""
    hashids = Hashids(salt=salt, min_length=min_length)
    return f'{base_url}s/{hashids.encode(obj_id)}'
