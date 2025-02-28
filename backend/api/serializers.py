"""Сериализаторы для приложения api."""

from django.core.validators import MinValueValidator
from django.db import transaction
from rest_framework import serializers

from core.utils import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.serializers import UserViewSerializer


class BaseIngredientRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для ингридиентов в рецепте."""

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class BaseRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для рецептов."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингридиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeViewSerializer(BaseIngredientRecipeSerializer):
    """Сериализатор для отображения ингридиентов в рецепте."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta(BaseIngredientRecipeSerializer.Meta):
        fields = BaseIngredientRecipeSerializer.Meta.fields + (
            'name',
            'measurement_unit',
        )


class IngredientRecipeAddSerializer(BaseIngredientRecipeSerializer):
    """Сериализатор для добавления ингридиентов в рецепт."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(validators=(MinValueValidator(1),))


class RecipeViewSerializer(BaseRecipeSerializer):
    """Сериализатор для просмотра рецептов."""

    tags = TagSerializer(many=True, read_only=True)
    author = UserViewSerializer(read_only=True)
    ingredients = IngredientRecipeViewSerializer(
        source='recipe_ingredients', many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields + (
            'is_favorited',
            'is_in_shopping_cart',
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.favorite_recipes.filter(id=obj.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.shopping_cart.filter(id=obj.id).exists()
        )


class RecipeCreateSerializer(BaseRecipeSerializer):
    """Сериализатор для создания и обновления рецептов."""

    author = UserViewSerializer(read_only=True)
    image = Base64ImageField(required=True)
    ingredients = IngredientRecipeAddSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    cooking_time = serializers.IntegerField(validators=(MinValueValidator(1),))

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields
        read_only_fields = ('author',)

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                'Должен присутствовать хотя бы один тег'
            )
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError('Теги не должны повторяться')
        return tags

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Должен присутствовать хотя бы один ингредиент'
            )
        ingredient_ids = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Ингредиенты не должны повторяться.'
            )
        return ingredients

    def get_ingredients(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user, **validated_data
        )
        recipe.tags.set(tags)
        self.get_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        missing_fields = [
            field
            for field in ('tags', 'ingredients')
            if field not in validated_data
        ]
        if missing_fields:
            raise serializers.ValidationError(
                {field: 'Обязательное поле.' for field in missing_fields}
            )

        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        instance = super().update(instance, validated_data)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        self.get_ingredients(instance, ingredients)
        return instance

    def to_representation(self, instance):
        return RecipeViewSerializer(instance, context=self.context).data
