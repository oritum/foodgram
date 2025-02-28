"""Views для приложения api."""

from collections import Counter
from datetime import datetime

from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from hashids import Hashids
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.base_views import BaseTagIngredientViewSet
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeViewSerializer,
    TagSerializer,
)
from api.utils import generate_shopping_list_pdf
from core.base_views import BaseUserRecipeManagementViewSet
from core.pagination import UsersRecipePagination
from core.utils import generate_short_link
from recipes.models import Ingredient, Recipe, Tag
from users.serializers import RecipeShortSerializer


def redirect_short_link(request, short_link):
    """Обработчик короткой ссылки."""

    recipe_id = Hashids(salt=settings.SHORTLINK_SALT, min_length=3).decode(
        short_link
    )
    if recipe_id:
        recipe = get_object_or_404(Recipe, id=recipe_id[0])
        return redirect(f'/recipes/{recipe.id}/')
    else:
        return redirect('/404/')


class RecipeManagementViewSet(BaseUserRecipeManagementViewSet):
    """
    ViewSet для управления рецептами.

    Предоставляет следующие действия:
    - list: получить список рецептов (доступно всем).
    - retrieve: получить конкретный рецепт по ID (доступно всем).
    - create: создать новый рецепт (требуется аутентификация).
    - update: обновить рецепт по ID (требуется аутентификация).
    - partial_update: частично обновить рецепт по ID (требуется
      аутентификация).
    - destroy: удалить рецепт по ID (требуется аутентификация).

    Дополнительные пользовательские действия:
    - favorite: добавить или удалить рецепт из избранного (требуется
      аутентификация).
    - shopping_cart: добавить или удалить рецепт из списка покупок, скачать
      список покупок файлом (требуется аутентификация).
    - get_link: получить короткую ссылку на рецепт (доступно всем).
    - download_shopping_cart: скачать список покупок файлом (требуется
      аутентификация).
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    pagination_class = UsersRecipePagination
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)
    open_actions = {'list', 'retrieve', 'get_link'}
    authenticated_actions = {
        'create',
        'favorite',
        'shopping_cart',
        'download_shopping_cart',
    }
    restricted_actions = {'update', 'partial_update', 'destroy'}
    restricted_permission = IsAuthorOrReadOnly
    serializer_map = {'get': RecipeViewSerializer}
    default_serializer = RecipeCreateSerializer

    def _handle_action(
        self, request, pk, related_name, add_error, remove_error
    ):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        related_manager = getattr(user, related_name)
        if request.method == 'POST':
            if related_manager.filter(id=recipe.id).exists():
                raise ValidationError(add_error)
            related_manager.add(recipe)
            serializer = RecipeShortSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not related_manager.filter(id=recipe.id).exists():
            raise ValidationError(remove_error)
        related_manager.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=('POST', 'DELETE'), detail=True, url_path='favorite')
    def favorite(self, request, pk=None):
        return self._handle_action(
            request,
            pk,
            'favorite_recipes',
            'Рецепт уже добавлен в избранное.',
            'Рецепт не найден в избранном.',
        )

    @action(methods=('POST', 'DELETE'), detail=True, url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        return self._handle_action(
            request,
            pk,
            'shopping_cart',
            'Рецепт уже добавлен в список покупок.',
            'Рецепт не найден в списке покупок.',
        )

    @action(
        methods=('GET',),
        detail=True,
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        return JsonResponse(
            {
                'short-link': generate_short_link(
                    get_object_or_404(Recipe, id=pk).id,
                    request.build_absolute_uri('/'),
                )
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=('GET',),
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart_recipes = user.shopping_cart.prefetch_related(
            'recipe_ingredients__ingredient'
        )
        ingredients = Counter()
        for recipe in shopping_cart_recipes:
            for recipe_ingredient in recipe.recipe_ingredients.all():
                key = (
                    recipe_ingredient.ingredient.name,
                    recipe_ingredient.ingredient.measurement_unit,
                )
                ingredients[key] += recipe_ingredient.amount
        if not ingredients:
            return Response(
                {'detail': 'Список покупок пуст'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return FileResponse(
            generate_shopping_list_pdf(ingredients),
            as_attachment=True,
            filename=f'shopping_list_{user.username}'
            f'_{datetime.now().strftime("%Y-%m-%d")}.pdf',
        )


class TagViewSet(BaseTagIngredientViewSet):
    """View для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseTagIngredientViewSet):
    """View для работы с ингредиентами."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
