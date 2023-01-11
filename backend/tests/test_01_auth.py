from rest_framework import status

import pytest

from .conftest import VALID_EMAIL, VALID_PASSWORD


class TestAuthorization:
    URL_LOGIN = '/api/auth/token/login/'
    URL_LOGOUT = '/api/auth/token/logout/'

    def test_00_auth_urls_not_404(self, client, user_client):
        urls = [self.URL_LOGIN, self.URL_LOGOUT]

        for url in urls:
            response = client.get(url)
            assert (
                response.status_code != status.HTTP_404_NOT_FOUND
            ), f'Страница `{url}` не найдена'

    @pytest.mark.django_db(transaction=True)
    def test_01_invalid_data_get_token(self, client):
        invalid_password = 'qwerty12345'
        invalid_email = 'invalid_username@gmail.com'
        invalid_data = {'password': invalid_password, 'email': invalid_email}
        response = client.post(self.URL_LOGIN, data=invalid_data)

        assert (
            response.status_code != status.HTTP_201_CREATED
        ), 'Выдан токен на невалидные данные'

        invalid_password = {'password': invalid_password, 'email': VALID_EMAIL}
        response = client.post(self.URL_LOGIN, data=invalid_password)

        assert (
            response.status_code != status.HTTP_201_CREATED
        ), 'Выдан токен на невалидный пароль'

        invalid_email = {'password': VALID_PASSWORD, 'email': invalid_email}
        response = client.post(self.URL_LOGIN, data=invalid_email)

        assert (
            response.status_code != status.HTTP_201_CREATED
        ), 'Выдан токен на невалидный email'

    @pytest.mark.django_db(transaction=True)
    def test_02_valid_data_get_token(self, client, user):
        valid_data = {'password': VALID_PASSWORD, 'email': VALID_EMAIL}

        response = client.post(self.URL_LOGIN, data=valid_data)
        assert (
            response.status_code == status.HTTP_201_CREATED
        ), 'Не выдан токен на валидные данные'

    @pytest.mark.django_db(transaction=True)
    def test_03_remove_token_auth(self, user_client):
        response = user_client.post(self.URL_LOGOUT)

        assert (
            response.status_code == status.HTTP_204_NO_CONTENT
        ), 'Не удаляется токен у авторезированного пользователя'

    @pytest.mark.django_db(transaction=True)
    def test_04_remove_token_not_auth(self, client):
        response = client.post(self.URL_LOGOUT)

        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
        ), 'Неавторезированного пользователя допускает до удаления токена'
