"""Views для приложения users."""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.base_views import BaseUserRecipeManagementViewSet
from core.pagination import UsersRecipePagination
from recipes.models import User
from users.serializers import (
    AvatarSerializer,
    SetPasswordSerializer,
    SubscriptionSerializer,
    UserCreateSerializer,
    UserViewSerializer,
)


class UserManagementViewSet(BaseUserRecipeManagementViewSet):
    """
    ViewSet для управления пользователями и подписками.

    Предоставляет следующие действия:
    - list: получить список пользователей (доступно всем).
    - retrieve: получить конкретного пользователя по ID (доступно всем).
    - create: создать нового пользователя (доступно всем).

    Дополнительные пользовательские действия:
    - me: получить данные аутентифицированного пользователя (требуется
      аутентификация).
    - set_password: изменить пароль аутентифицированного пользователя
      (требуется аутентификация).
    - avatar: обновить или удалить аватар аутентифицированного пользователя
      (требуется аутентификация).
    - subscriptions: получить список подписок аутентифицированного пользователя
      (требуется аутентификация).
    - subscribe: подписаться или отписаться от пользователя по ID (требуется
      аутентификация).
    """

    queryset = User.objects.all()
    pagination_class = UsersRecipePagination
    lookup_field = 'id'
    search_fields = (
        'username',
        'email',
    )
    open_actions = {'list', 'retrieve', 'create'}
    authenticated_actions = {
        'me',
        'set_password',
        'avatar',
        'subscriptions',
        'subscribe',
    }
    serializer_map = {
        'create': UserCreateSerializer,
        'subscriptions': SubscriptionSerializer,
        'subscribe': SubscriptionSerializer,
    }
    default_serializer = UserViewSerializer

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    @action(
        methods=('POST',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='set_password',
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(
            {'detail': 'Пароль успешно изменён'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        methods=(
            'PUT',
            'DELETE',
        ),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me/avatar',
    )
    def avatar(self, request):
        return (
            self._update_avatar(request)
            if request.method == 'PUT'
            else self._delete_avatar(request)
        )

    def _update_avatar(self, request):
        serializer = AvatarSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _delete_avatar(self, request):
        request.user.avatar = None
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        subscriptions = request.user.subscriptions.all()
        page = self.paginate_queryset(subscriptions)
        serializer = (
            self.get_serializer(page, many=True)
            if page
            else self.get_serializer(subscriptions, many=True)
        )
        return (
            self.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data)
        )

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path='subscribe',
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return self._error_response('Нельзя подписаться на самого себя.')
        if request.method == 'POST':
            return self._subscribe(user, author)
        return self._unsubscribe(user, author)

    def _subscribe(self, user, author):
        if user.subscriptions.filter(id=author.id).exists():
            return self._error_response(
                'Вы уже подписаны на этого пользователя.'
            )
        user.subscriptions.add(author)
        serializer = self.get_serializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _unsubscribe(self, user, author):
        if not user.subscriptions.filter(id=author.id).exists():
            return self._error_response(
                'Вы не подписаны на этого пользователя.'
            )
        user.subscriptions.remove(author)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _error_response(self, message):
        return Response(
            {'detail': message}, status=status.HTTP_400_BAD_REQUEST
        )
