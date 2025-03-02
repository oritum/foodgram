"""Сериализаторы для приложения users."""

from rest_framework import serializers

from core.utils import Base64ImageField
from recipes.models import Recipe, User


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserViewSerializer(BaseUserSerializer):
    """Сериализатор для просмотра пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            'is_subscribed',
            'avatar',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.subscribers.filter(id=request.user.id).exists()


class UserCreateSerializer(BaseUserSerializer):
    """Сериализатор для создания пользователей."""

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation


class AvatarSerializer(BaseUserSerializer):
    """Сериализатор для работы с аватаром пользователя."""

    avatar = Base64ImageField(required=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ('avatar',)


class SetPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Текущий пароль указан неверно.')
        return value


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения краткой информации о рецепте."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionSerializer(BaseUserSerializer):
    """Сериализатор для подписок пользователя."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + (
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )
        read_only_fields = ('id', 'username')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return (
            user.is_authenticated
            and obj.subscribers.filter(id=user.id).exists()
        )

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )
        recipes = (
            # fmt: off
            obj.recipes.all()[:int(recipes_limit)]
            # fmt: on
            if recipes_limit
            else obj.recipes.all()
        )
        return RecipeShortSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
