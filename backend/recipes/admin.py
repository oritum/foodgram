from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Регистрация модели ингредиента в админке."""

    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)


class RecipeIngredientAdmin(admin.StackedInline):
    """Регистрация модели промежуточной таблицы в админке."""

    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Регистрация модели тега в админке."""

    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Регистрация модели рецепта в админке."""

    list_display = (
        'name',
        'text',
        'author',
        'display_tags',
        'display_ingredients',
        'favorite_count',
        'pub_date',
    )
    search_fields = (
        'name',
        'author__username',
    )
    list_filter = ('tags',)

    inlines = (RecipeIngredientAdmin,)

    def display_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    display_tags.short_description = 'Теги'

    def display_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )

    display_ingredients.short_description = 'Ингредиенты'
