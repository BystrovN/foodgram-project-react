from rest_framework import status
import pytest

from .conftest import NAME, MAIN_ID


class TestTags:
    URL_TAGS = '/api/tags/'
    URL_VALID_TAG = f'/api/tags/{MAIN_ID}/'
    URL_INVALID_TAG = '/api/tags/100/'

    @pytest.mark.django_db(transaction=True)
    def test_00_get_tags(self, client, tag):
        urls_status = {
            self.URL_TAGS: status.HTTP_200_OK,
            self.URL_VALID_TAG: status.HTTP_200_OK,
            self.URL_INVALID_TAG: status.HTTP_404_NOT_FOUND,
        }

        for url, stat in urls_status.items():
            response = client.get(url)
            assert (
                response.status_code == stat
            ), f'Ошибка в статусе {url}, пользователь неавторизован'

    @pytest.mark.django_db(transaction=True)
    def test_01_get_tag_content_check(self, client, tag):
        response = client.get(self.URL_VALID_TAG)
        response_json = response.json()

        assert (
            response_json.get('name') == NAME
        ), f'{self.URL_VALID_TAG} возвращает некорректные данные '
