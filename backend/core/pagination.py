"""Пагинаторы для проекта foodgram_backend."""

from rest_framework.pagination import PageNumberPagination


class UsersRecipePagination(PageNumberPagination):
    """Пагинатор для пользователей и рецептов."""

    page_size_query_param = 'limit'
    page_size = 6
