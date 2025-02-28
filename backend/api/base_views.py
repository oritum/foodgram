"""Базовые View для приложения api."""

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet


class BaseTagIngredientViewSet(ModelViewSet):
    """Базовый ViewSet для тегов и ингридиентов."""

    permission_classes = (AllowAny,)
    http_method_names = ('get',)
