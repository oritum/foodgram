"""Утилиты для проекта foodgram_backend."""

import base64
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from hashids import Hashids
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Поле для работы с изображениями в формате base64."""

    def to_internal_value(self, data: str) -> ContentFile:
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}'
            )
        return super().to_internal_value(data)

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
    return f'{base_url}/s/{hashids.encode(obj_id)}'
