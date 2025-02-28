"""Фильтры для моделей приложения api."""

from django.db.models import Case, IntegerField, When
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Tag


class RecipeFilter(filters.FilterSet):
    """Фильтры для рецептов."""

    author = filters.CharFilter(
        field_name='author__id',
        lookup_expr='exact',
        label='Автор',
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        label='Теги',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
        label='В избранном',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
        label='В списке покупок',
    )

    def filter_by_user_related_field(
        self, queryset, name, value, related_field
    ):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none() if value else queryset
        if value:
            return queryset.filter(**{related_field: user})
        return queryset.exclude(**{related_field: user})

    def filter_is_favorited(self, queryset, name, value):
        return self.filter_by_user_related_field(
            queryset, name, value, 'favorite_recipes'
        )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self.filter_by_user_related_field(
            queryset, name, value, 'shopping_cart_recipes'
        )


class IngredientFilter(filters.FilterSet):
    """Фильтры для ингредиентов."""

    name = filters.CharFilter(
        method='filter_by_name',
        label='Название',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)

    def filter_by_name(self, queryset, name, value):
        return (
            queryset.filter(name__icontains=value)
            .annotate(
                priority=Case(
                    When(name__istartswith=value, then=0),
                    default=1,
                    output_field=IntegerField(),
                )
            )
            .order_by('priority', 'name')
        )
