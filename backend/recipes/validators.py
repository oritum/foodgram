"""Валидаторы для приложения recipes."""

import re

from django.core.exceptions import ValidationError


def validate_slug(value: str) -> str:
    """Валидация для поля slug в модели Tag."""
    pattern = r'^[-a-zA-Z0-9_]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'slug может содержать только буквы (a-z, A-Z), '
            'цифры (0-9) и символы "-" и "_"'
        )
    return value
