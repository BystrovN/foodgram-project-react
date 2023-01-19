from rest_framework import status
import pytest

from recipes.models import ShoppingList
from .conftest import MAIN_ID


class TestFavorite:
    URL_SHOP_RECIPE = f'/api/recipes/{MAIN_ID}/shopping_cart/'

    @pytest.mark.django_db(transaction=True)
    def test_00_add_shop(self, user_client, recipe, user):
        instance = ShoppingList.objects.filter(user=user, recipe=recipe)
        assert instance.exists() is False

        response = user_client.post(self.URL_SHOP_RECIPE)
        assert response.status_code == status.HTTP_201_CREATED

        assert instance.exists() is True

    @pytest.mark.django_db(transaction=True)
    def test_01_add_shop_the_same(self, user_client, shop_recipe):
        response = user_client.post(self.URL_SHOP_RECIPE)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db(transaction=True)
    def test_02_delete_shop(self, user_client, shop_recipe, user, recipe):
        instance = ShoppingList.objects.filter(user=user, recipe=recipe)
        assert instance.exists() is True

        response = user_client.delete(self.URL_SHOP_RECIPE)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert instance.exists() is False

        response = user_client.delete(self.URL_SHOP_RECIPE)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_03_shop_unauth(self, client):
        responses = (client.post, client.delete)

        for res in responses:
            response = res(self.URL_SHOP_RECIPE)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
