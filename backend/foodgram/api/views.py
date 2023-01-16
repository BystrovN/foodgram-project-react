from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from recipes.models import Tag, Ingredient, Recipe
from users.paginations import CustomPageNumberPagination
from . import serializers
from .permissions import AuthorOrAdminOrReadOnly
from .filters import RecipeFilter

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
        qs = [i for i in qs_contains if i not in qs_startswith]
        qs = qs_startswith + qs

        return qs


class RecipesViewSet(ModelViewSet):
    """Представление для модели Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (AuthorOrAdminOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    ]
