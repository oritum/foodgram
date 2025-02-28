"""Базовые Views для проекта foodgram_backend."""

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class BaseUserRecipeManagementViewSet(ModelViewSet):
    """Базовый ViewSet для управления пользователями и рецептами."""

    def get_permissions(self):
        if self.action in self.open_actions:
            return (AllowAny(),)
        if self.action in self.authenticated_actions:
            return (IsAuthenticated(),)
        if (
            hasattr(self, 'restricted_actions')
            and self.action in self.restricted_actions
        ):
            return (self.restricted_permission(),)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.default_serializer)
