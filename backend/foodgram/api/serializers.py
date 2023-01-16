from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from users.serializers import UserSerializer
from .utils import is_favorited, is_in_shopping_cart

FAVORITED_KEY = 'is_favorited'
SHOPPING_CART_KEY = 'is_in_shopping_cart'


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер тегов."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер ингридиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для использования в качестве поля в RecipeSerializer."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер рецептов."""

    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            FAVORITED_KEY,
            SHOPPING_CART_KEY,
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def _get_user(self):
        return self.context.get('request').user

    def get_ingredients(self, obj):
        qs = obj.recipe_ingredient.all()
        return RecipeIngredientSerializer(qs, many=True).data

    def get_is_favorited(self, obj):
        return is_favorited(self._get_user(), obj.id)

    def get_is_in_shopping_cart(self, obj):
        return is_in_shopping_cart(self._get_user(), obj.id)
