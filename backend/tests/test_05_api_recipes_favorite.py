from rest_framework import status
import pytest

from .conftest import MAIN_ID
from recipes.models import FavoriteList


class TestFavorite:
    URL_FAV_RECIPE = f'/api/recipes/{MAIN_ID}/favorite/'

    @pytest.mark.django_db(transaction=True)
    def test_00_add_fav(self, user_client, recipe, user):
        instance = FavoriteList.objects.filter(user=user, recipe=recipe)
        assert instance.exists() is False

        response = user_client.post(self.URL_FAV_RECIPE)
        assert response.status_code == status.HTTP_201_CREATED

        assert instance.exists() is True

    @pytest.mark.django_db(transaction=True)
    def test_01_add_fav_the_same(self, user_client, fav_recipe):
        response = user_client.post(self.URL_FAV_RECIPE)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db(transaction=True)
    def test_02_delete_fav(self, user_client, fav_recipe, user, recipe):
        instance = FavoriteList.objects.filter(user=user, recipe=recipe)
        assert instance.exists() is True

        response = user_client.delete(self.URL_FAV_RECIPE)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert instance.exists() is False

        response = user_client.delete(self.URL_FAV_RECIPE)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_03_fav_unauth(self, client):
        responses = (client.post, client.delete)

        for res in responses:
            response = res(self.URL_FAV_RECIPE)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
