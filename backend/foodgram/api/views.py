from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from recipes.models import Tag, Ingredient, Recipe, FavoriteList, ShoppingList
from users.paginations import CustomPageNumberPagination
from . import serializers
from .permissions import AuthorOrAdminOrReadOnly
from .filters import RecipeFilter
from .utils import (
    is_favorited,
    is_in_shopping_cart,
    get_ingredients_from_shopping_cart,
)
from .exceptions import (
    FavoriteException,
    ShoppingCartException,
    EmptyShoppingCart,
)

User = get_user_model()


class TagsViewSet(ReadOnlyModelViewSet):
    """Представление для вывода списка и экземпляра тега."""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (AllowAny,)


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Представление для вывода списка и экземпляра ингридиента."""

    serializer_class = serializers.IngredientSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        """
        Регистронезависимый поиск по полю name по вхождению в начало
        названия и по вхождению в произвольном месте. Приоритет в выдаче
        при совпадении в начале названия.
        """
        search_name = self.request.query_params.get('search')

        if not search_name:
            return Ingredient.objects.all()

        qs_startswith = list(
            Ingredient.objects.filter(
                Q(name__istartswith=search_name),
            )
        )
        qs_contains = list(
            Ingredient.objects.filter(
                Q(name__icontains=search_name),
            )
        )
        queryset = [i for i in qs_contains if i not in qs_startswith]
        queryset = qs_startswith + queryset

        return queryset


class RecipesViewSet(ModelViewSet):
    """Представление для модели Recipe."""

    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrAdminOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
        'trace',
    ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeSerializer

        return serializers.CreateRecipeSerializer

    def _create(self, user, recipe, model):
        obj = model.objects.create(user=user, recipe=recipe)
        obj.save()
        serializer = serializers.ShortRecipesSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete(self, user, recipe, model):
        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if is_favorited(request, recipe.id):
            raise FavoriteException(f'Рецепт {recipe} уже в избранном')

        return self._create(request.user, recipe, FavoriteList)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if not is_favorited(request, recipe.id):
            raise FavoriteException(f'Рецепт {recipe} не в избранном')

        return self._delete(request.user, recipe, FavoriteList)

    @action(methods=['post'], detail=True)
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if is_in_shopping_cart(request, recipe.id):
            raise ShoppingCartException(f'Рецепт {recipe} уже в корзине')

        return self._create(request.user, recipe, ShoppingList)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if not is_in_shopping_cart(request, recipe.id):
            raise ShoppingCartException(f'Рецепт {recipe} не в корзине')

        return self._delete(request.user, recipe, ShoppingList)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        name = 0
        measure = 1
        amount = 2

        ingredients = get_ingredients_from_shopping_cart(request.user)
        if not ingredients:
            raise EmptyShoppingCart

        cart = ''
        ingredients = [*ingredients]
        for ing in ingredients:
            cart += f'{ing[name]} ({ing[measure]}) - {ing[amount]} \n'
        response = HttpResponse(cart, content_type='text/plain')

        return response
