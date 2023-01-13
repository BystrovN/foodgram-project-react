import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

VALID_PASSWORD = '12345'
VALID_EMAIL = 'testuser@gmail.com'
VALID_USERNAME = 'TestUser'
MAIN_USER_ID = 1


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username=VALID_USERNAME,
        password=VALID_PASSWORD,
        email=VALID_EMAIL,
        first_name='Test',
        last_name='User',
        id=MAIN_USER_ID
    )


@pytest.fixture
def user_client(user):
    token = Token.objects.create(user=user)
    token.key
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def two_followers(django_user_model):
    return django_user_model.objects.bulk_create(
        django_user_model(
            email=f'test{i}@test.com',
            username=f'Test{i}',
            password='12345678',
            first_name=f'Test{i}',
            last_name=f'Test{i}',
            id=MAIN_USER_ID + 1 + i
        )
        for i in range(2)
    )
