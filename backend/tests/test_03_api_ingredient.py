from rest_framework import status
import pytest

from .conftest import NAME, MAIN_ID, NEW_OBJECTS_QUANTITY


class TestIngredients:
    URL_INGREDIENTS = '/api/ingredients/'
    URL_VALID_INGREDIENT = f'/api/ingredients/{MAIN_ID}/'
    URL_INVALID_INGREDIENT = '/api/ingredients/100/'

    @pytest.mark.django_db(transaction=True)
    def test_00_get_ingredients(self, client, five_ingredients):
        urls_status = {
            self.URL_INGREDIENTS: status.HTTP_200_OK,
            self.URL_VALID_INGREDIENT: status.HTTP_200_OK,
            self.URL_INVALID_INGREDIENT: status.HTTP_404_NOT_FOUND,
        }

        for url, stat in urls_status.items():
            response = client.get(url)
            assert (
                response.status_code == stat
            ), f'Ошибка в статусе {url}, пользователь неавторизован'

    @pytest.mark.django_db(transaction=True)
    def test_01_get_ingredient_content_check(self, client, five_ingredients):
        response = client.get(self.URL_VALID_INGREDIENT)
        response_json = response.json()

        assert (
            response_json.get('name') == NAME
        ), f'{self.URL_VALID_TAG} возвращает некорректные данные '

    @pytest.mark.django_db(transaction=True)
    def test_02_ingredient_search_check(self, client, five_ingredients):
        response = client.get(f'{self.URL_INGREDIENTS}?search=test')
        response_json = response.json()

        assert response_json[0].get('name') == NAME
        assert response_json[1].get('name') == 'XIngTest0X'
        assert len(response_json) == NEW_OBJECTS_QUANTITY + 1
