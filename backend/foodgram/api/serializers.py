import base64

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile

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
    """Сериалайзер просмотра рецептов."""

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

    def _get_request(self):
        return self.context.get('request')

    def get_ingredients(self, obj):
        qs = obj.recipe_ingredient.all()
        return RecipeIngredientSerializer(qs, many=True).data

    def get_is_favorited(self, obj):
        return is_favorited(self._get_request(), obj.id)

    def get_is_in_shopping_cart(self, obj):
        return is_in_shopping_cart(self._get_request(), obj.id)


class AddIngredientToRecipeSerializer(serializers.Serializer):
    """
    Сериалайзер для использования в качестве поля в CreateRecipeSerializer.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')

        return super().to_internal_value(data)


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер создания рецептов."""

    ingredients = AddIngredientToRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
            'author',
        )
        read_only_fields = ('author',)

    def _add_ingredients(seld, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_instance = ingredient.get('id')
            amount = ingredient.get('amount')
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_instance,
                amount=amount,
            )

    def _put_validate(self, attrs):
        required_fields = (
            'tags',
            'name',
            'text',
            'cooking_time',
            'ingredients',
            'image',
        )
        for field in required_fields:
            try:
                attrs[field]
            except KeyError:
                raise ValidationError(f'Не передано обязательное поле {field}')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            **validated_data,
            author_id=self.root.context.get('request').user.id,
        )
        recipe.tags.set(tags)
        self._add_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.image = validated_data.get('image')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.tags.clear()
        instance.tags.set(validated_data.get('tags'))
        instance.ingredients.clear()
        self._add_ingredients(validated_data.get('ingredients'), instance)

        return instance

    def validate(self, attrs):
        self._put_validate(attrs)

        ingredients = attrs.get('ingredients')
        unique_ingredients = []
        for ingredient in ingredients:
            instance = ingredient.get('id')
            RecipeIngredientSerializer(data=ingredient).is_valid(
                raise_exception=True
            )
            if instance in unique_ingredients:
                raise ValidationError(
                    {'ingredients': f'Дублирование ингридиента {instance}'}
                )
            unique_ingredients.append(instance)

        return attrs

    def to_representation(self, value):
        return RecipeSerializer(value).data
