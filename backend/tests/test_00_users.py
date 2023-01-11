import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

from users.models import Follow
from users.serializers import IS_SUBSCRIBED_KEY

User = get_user_model()


class TestUsers:
    URL_LIST_USERS = '/api/users/'
    URL_VALID_INSTANCE_USER = '/api/users/1/'
    URL_INVALID_INSTANCE_USER = '/api/users/100/'

    def test_00_get_valid_users_urls_available(self, client, user_client):
        urls = [self.URL_LIST_USERS, self.URL_VALID_INSTANCE_USER]

        for url in urls:
            response = client.get(url)
            assert (
                response.status_code == status.HTTP_200_OK
            ), f'Страница `{url}` недоступна неавторезированному'

        for url in urls:
            response = user_client.get(url)
            assert (
                response.status_code == status.HTTP_200_OK
            ), f'Страница `{url}` недоступна авторезированному'

    @pytest.mark.django_db(transaction=True)
    def test_01_get_invalid_users_urls_unavailable(self, client):
        response = client.get(self.URL_INVALID_INSTANCE_USER)
        assert (
            response.status_code == status.HTTP_404_NOT_FOUND
        ), 'Невалидная страница пользователя доступна'

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
    def test_04_is_subscribed(self, client, user_client):
        following_id = 3
        not_following_id = 4
        new_users_quantity = 3

        User.objects.bulk_create(
            User(
                email=f'test{i}@test.com',
                username=f'Test{i}',
                password='12345678',
                first_name=f'Test{i}',
                last_name=f'Test{i}',
            )
            for i in range(new_users_quantity)
        )

        follower = User.objects.get(id=2)  # У TestUser из conftest.py id = 2
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
        ), 'API возвращает is_subscribed = True на анонима'
