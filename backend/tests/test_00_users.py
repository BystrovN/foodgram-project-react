import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

from users.models import Follow
from users.serializers import IS_SUBSCRIBED_KEY

from .conftest import USER_EMAIL, USER_PASSWORD, NAME, MAIN_ID

User = get_user_model()


class TestUsers:
    URL_LIST_USERS = '/api/users/'
    URL_VALID_INSTANCE_USER = f'/api/users/{MAIN_ID}/'
    URL_INVALID_INSTANCE_USER = '/api/users/100/'
    URL_ME = '/api/users/me/'
    URL_SET_PASSWORD = '/api/users/set_password/'
    URL_SUBSCRIPTIONS = '/api/users/subscriptions/'

    @pytest.mark.django_db(transaction=True)
    def test_00_check_users_urls_auth(self, user_client, client):
        urls_status = {
            self.URL_LIST_USERS: status.HTTP_200_OK,
            self.URL_VALID_INSTANCE_USER: status.HTTP_200_OK,
            self.URL_SUBSCRIPTIONS: status.HTTP_200_OK,
            self.URL_ME: status.HTTP_200_OK,
        }

        for url, stat in urls_status.items():
            response = user_client.get(url)
            assert (
                response.status_code == stat
            ), f'Ошибка в статусе {url}, пользователь авторизован'

    @pytest.mark.django_db(transaction=True)
    def test_01_check_users_urls_unauth(self, user_client, client):

        urls_status = {
            self.URL_LIST_USERS: status.HTTP_200_OK,
            self.URL_VALID_INSTANCE_USER: status.HTTP_200_OK,
            self.URL_INVALID_INSTANCE_USER: status.HTTP_404_NOT_FOUND,
            self.URL_ME: status.HTTP_401_UNAUTHORIZED,
            self.URL_SET_PASSWORD: status.HTTP_401_UNAUTHORIZED,
            self.URL_SUBSCRIPTIONS: status.HTTP_401_UNAUTHORIZED,
        }

        for url, stat in urls_status.items():
            response = client.get(url)
            assert (
                response.status_code == stat
            ), f'Ошибка в статусе {url}, пользователь неавторизован'

    @pytest.mark.django_db(transaction=True)
    def test_02_post_valid_users_urls(self, client):
        username = 'Test'
        data = {
            'email': 'test@test.com',
            'username': username,
            'password': '12345678',
            'first_name': 'Test',
            'last_name': 'Test',
            'id': 1,
        }

        assert User.objects.filter(username=username).exists() is False

        response = client.post(self.URL_LIST_USERS, data=data)

        assert (
            response.status_code == status.HTTP_201_CREATED
        ), 'Пользователь с валидными данными не создается'
        assert (
            User.objects.filter(username=username).exists() is True
        ), 'Пользователь с валидными данными не создается'

    @pytest.mark.django_db(transaction=True)
    def test_03_post_invalid_users_urls(self, client):
        data = {
            'email': 'Invalid',
            'username': 'invalid@test.com',
            'password': '12345678',
            'first_name': 'Test',
            'last_name': 'Test',
        }
        response = client.post(self.URL_LIST_USERS, data=data)

        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), 'Пользователь с невалидными данными создается'

    @pytest.mark.django_db(transaction=True)
    def test_04_is_subscribed(self, client, user_client, two_followers):
        following_id = MAIN_ID + 1
        not_following_id = MAIN_ID + 2

        follower = User.objects.get(id=MAIN_ID)
        author = User.objects.get(id=following_id)
        follow = Follow.objects.create(user=follower, author=author)

        response = user_client.get(f'/api/users/{not_following_id}/')
        response_json = response.json()
        assert (
            response_json.get(IS_SUBSCRIBED_KEY) is False
        ), 'API возвращает is_subscribed = True на неподписанного пользователя'

        response = user_client.get(f'/api/users/{following_id}/')
        response_json = response.json()
        assert (
            response_json.get(IS_SUBSCRIBED_KEY) is True
        ), 'API возвращает is_subscribed = False на подписанного пользователя'

        response = user_client.get(self.URL_SUBSCRIPTIONS)
        response_json = response.json()
        assert (
            response_json.get('results')[0].get('username') == 'Test0'
        ), 'Ответ {self.URL_SUBSCRIPTIONS} не корректный'

        follow.delete()
        response = user_client.get(f'/api/users/{following_id}/')
        response_json = response.json()
        assert (
            response_json.get(IS_SUBSCRIBED_KEY) is False
        ), 'API возвращает is_subscribed = True на неподписанного пользователя'

        response = client.get(f'/api/users/{following_id}/')
        response_json = response.json()
        assert (
            response_json.get(IS_SUBSCRIBED_KEY) is False
        ), 'API возвращает is_subscribed = True на неавторизованного'

        response = user_client.get(self.URL_SUBSCRIPTIONS)
        response_json = response.json()

        assert (
            len(response_json.get('results')) == 0
        ), 'Ответ {self.URL_SUBSCRIPTIONS} не корректный. Список не пустой'

    def test_05_get_me_auth(self, user_client):
        response = user_client.get(self.URL_ME)
        response_json = response.json()

        assert (
            response_json.get('email') == USER_EMAIL
        ), 'api/users/me возвращает некорректные данные '

    def test_06_set_password_auth(self, user_client):
        data = {
            'new_password': 'qwerty',
            'current_password': USER_PASSWORD,
        }
        response = user_client.post(self.URL_SET_PASSWORD, data=data)

        assert (
            response.status_code == status.HTTP_204_NO_CONTENT
        ), 'Пароль не изменяется у авторизованного'

    def test_07_get_users_content_check(self, user_client):
        response = user_client.get(self.URL_LIST_USERS)
        response_json = response.json()

        assert response_json.get('results')[0].get('username') == NAME

    def test_08_get_instant_user_content_check(self, user_client):
        response = user_client.get(self.URL_VALID_INSTANCE_USER)
        response_json = response.json()

        assert response_json.get('username') == NAME

    def test_09_subscribe(self, client, user_client, two_followers):
        following_author_id = MAIN_ID + 1
        invalid_id = 100

        response = user_client.post(
            f'/api/users/{following_author_id}/subscribe/'
        )
        assert response.status_code == status.HTTP_201_CREATED

        response = user_client.post(
            f'/api/users/{following_author_id}/subscribe/'
        )
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), 'API позволяет повторно подписаться, что запрещено'

        response = user_client.delete(
            f'/api/users/{following_author_id}/subscribe/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = user_client.post(f'/api/users/{MAIN_ID}/subscribe/')
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), 'API позволяет подписаться на себя самого, что запрещено'

        response = client.post(f'/api/users/{following_author_id}/subscribe/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = client.delete(
            f'/api/users/{following_author_id}/subscribe/'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = user_client.post(f'/api/users/{invalid_id}/subscribe/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = user_client.delete(f'/api/users/{invalid_id}/subscribe/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
