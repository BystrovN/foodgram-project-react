from django_filters import rest_framework

from recipes.models import Recipe, Tag, FavoriteList, ShoppingList
from .serializers import FAVORITED_KEY, SHOPPING_CART_KEY


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    author = rest_framework.NumberFilter(field_name='author__id')
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = (
            FAVORITED_KEY,
            SHOPPING_CART_KEY,
            'author',
            'tags',
        )

    def _many_to_many_recipe_filter(self, queryset, value, model):
        user = self.request.user
        if not user.is_authenticated:
            return Recipe.objects.none()

        filter_id = model.objects.values_list('recipe_id', flat=True).filter(
            user_id=user.id
        )
        if value:
            return queryset.filter(id__in=filter_id)

        return queryset.exclude(id__in=filter_id)

    def get_is_favorited(self, queryset, name, value):
        return self._many_to_many_recipe_filter(queryset, value, FavoriteList)

    def get_is_in_shopping_cart(self, queryset, name, value):
        return self._many_to_many_recipe_filter(queryset, value, ShoppingList)
