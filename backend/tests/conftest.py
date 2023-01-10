import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

VALID_PASSWORD = '12345'
VALID_EMAIL = 'testuser@gmail.com'


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        password=VALID_PASSWORD,
        email=VALID_EMAIL,
        first_name='Test',
        last_name='User',
    )


@pytest.fixture
def user_client(user):
    token = Token.objects.create(user=user)
    token.key
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client
