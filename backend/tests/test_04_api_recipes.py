from rest_framework import status
import pytest

from recipes.models import Recipe
from api.serializers import FAVORITED_KEY, SHOPPING_CART_KEY
from .conftest import MAIN_ID, IMAGE, NAME


class TestRecipes:
    URL_RECIPES = '/api/recipes/'
    URL_VALID_RECIPE = f'/api/recipes/{MAIN_ID}/'
    URL_INVALID_RECIPE = '/api/recipes/100/'
    VALID_DATA = {
        'tags': [1, 2],
        'name': 'TestRecipe',
        'text': 'TestText',
        'cooking_time': 2,
        'ingredients': [
            {'id': 1, 'amount': 12},
            {'id': 2, 'amount': 1},
        ],
        'image': IMAGE,
    }

    @pytest.mark.django_db(transaction=True)
    def test_00_create_patch_delete_recipe(
        self,
        user_client,
        tag,
        second_tag,
        five_ingredients,
    ):
        statuses_data = {
            status.HTTP_201_CREATED: self.VALID_DATA,
            status.HTTP_400_BAD_REQUEST: {
                'tags': self.VALID_DATA['tags'],
                'name': self.VALID_DATA['name'],
                'text': self.VALID_DATA['text'],
                'cooking_time': self.VALID_DATA['cooking_time'],
                'ingredients': self.VALID_DATA['ingredients'],
            },
            status.HTTP_400_BAD_REQUEST: {
                'tags': self.VALID_DATA['tags'],
                'name': self.VALID_DATA['name'],
                'text': self.VALID_DATA['text'],
                'cooking_time': self.VALID_DATA['cooking_time'],
                'ingredients': [{'id': 1, 'amount': 0}],
                'image': IMAGE,
            },
            status.HTTP_400_BAD_REQUEST: {
                'tags': self.VALID_DATA['tags'],
                'name': self.VALID_DATA['name'],
                'text': self.VALID_DATA['text'],
                'cooking_time': self.VALID_DATA['cooking_time'],
                'ingredients': [{'id': 100, 'amount': 1}],
                'image': IMAGE,
            },
            status.HTTP_400_BAD_REQUEST: {
                'tags': [100],
                'name': self.VALID_DATA['name'],
                'text': self.VALID_DATA['text'],
                'cooking_time': self.VALID_DATA['cooking_time'],
                'ingredients': self.VALID_DATA['ingredients'],
                'image': IMAGE,
            },
        }

        recipe = Recipe.objects.filter(
            name=self.VALID_DATA['name'], text=self.VALID_DATA['text']
        )
        assert recipe.exists() is False

        for stat, data in statuses_data.items():
            response = user_client.post(
                self.URL_RECIPES, data=data, format='json'
            )
            assert response.status_code == stat

        assert recipe.exists() is True

        del statuses_data[status.HTTP_201_CREATED]
        statuses_data[status.HTTP_200_OK] = self.VALID_DATA
        for stat, data in statuses_data.items():
            response = user_client.patch(
                self.URL_VALID_RECIPE, data=data, format='json'
            )
            assert response.status_code == stat

    @pytest.mark.django_db(transaction=True)
    def test_01_delete_recipe(self, user_client, second_user_client, recipe):
        statuses_client = {
            status.HTTP_403_FORBIDDEN: second_user_client,
            status.HTTP_204_NO_CONTENT: user_client,
        }
        for stat, client in statuses_client.items():
            response = client.delete(self.URL_VALID_RECIPE)

            assert response.status_code == stat

    @pytest.mark.django_db(transaction=True)
    def test_02_patch_recipe_not_author(self, second_user_client, recipe):
        response = second_user_client.patch(self.URL_VALID_RECIPE)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_03_recipe_unauth(self, client, recipe):
        allowed_urls_statuses = {
            self.URL_RECIPES: status.HTTP_200_OK,
            self.URL_VALID_RECIPE: status.HTTP_200_OK,
            self.URL_INVALID_RECIPE: status.HTTP_404_NOT_FOUND,
        }

        for url, stat in allowed_urls_statuses.items():
            response = client.get(url)
            assert response.status_code == stat

    def test_04_401(self, client, recipe):
        responses = (
            client.post(self.URL_RECIPES),
            client.patch(self.URL_VALID_RECIPE),
            client.delete(self.URL_VALID_RECIPE),
        )
        for response in responses:
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_05_search_author_id(self, client, recipe):
        response = client.get(f'{self.URL_RECIPES}?author=1')
        response_json = response.json().get('results')
        assert len(response_json) == 1
        assert response_json[0].get('author').get('username') == NAME

        response = client.get(f'{self.URL_RECIPES}?author=2')
        response_json = response.json().get('results')
        assert len(response_json) == 0

    def test_06_recipe_in_favorite(
        self, user_client, second_user_client, fav_recipe
    ):
        client_keys = {
            user_client: True,
            second_user_client: False
        }

        for client, key in client_keys.items():
            response = client.get(self.URL_VALID_RECIPE)
            response_json = response.json()
            assert response_json.get(FAVORITED_KEY) is key

    def test_07_recipe_in_shopping_cart(
        self, user_client, second_user_client, shop_recipe
    ):
        client_keys = {
            user_client: True,
            second_user_client: False
        }

        for client, key in client_keys.items():
            response = client.get(self.URL_VALID_RECIPE)
            response_json = response.json()
            assert response_json.get(SHOPPING_CART_KEY) is key
