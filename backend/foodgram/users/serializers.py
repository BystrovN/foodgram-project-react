from django.contrib.auth import get_user_model
from rest_framework import serializers

from .utils import is_subscribed, recipes_count, get_limit_recipes
from recipes.models import Recipe

User = get_user_model()
IS_SUBSCRIBED_KEY = 'is_subscribed'


class GetTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения пользователем токена."""

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(
        max_length=150, required=True, write_only=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер просмотра списка пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            IS_SUBSCRIBED_KEY,
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:  # Если пользователь переходит на api/users/me/
            return False

        return is_subscribed(request.user, obj.id)


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер создания экземпляра пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SetPasswordViewSerializer(serializers.Serializer):
    """Сериалайзер для смены пароля."""

    new_password = serializers.CharField(
        max_length=150, required=True, write_only=True
    )

    current_password = serializers.CharField(
        max_length=150, required=True, write_only=True
    )


class RecipesSubscriptionsSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для использования в качестве поля MySubscriptionsSerializer.
    """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class MySubscriptionsSerializer(UserSerializer):
    """Сериалайзер для просмотра собственных подписок пользователя."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            IS_SUBSCRIBED_KEY,
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return recipes_count(obj)

    def get_recipes(self, obj):
        qs = get_limit_recipes(self, obj)

        return RecipesSubscriptionsSerializer(qs, many=True).data
