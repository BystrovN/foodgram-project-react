import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from recipes.models import Tag, Ingredient

USER_PASSWORD = '12345'
USER_EMAIL = 'testuser@gmail.com'
NAME = 'TestTestTest'
MAIN_ID = 1
NEW_OBJECTS_QUANTITY = 3


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username=NAME,
        password=USER_PASSWORD,
        email=USER_EMAIL,
        first_name='Test',
        last_name='User',
        id=MAIN_ID,
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
            id=MAIN_ID + 1 + i,
        )
        for i in range(NEW_OBJECTS_QUANTITY)
    )


@pytest.fixture
def tag():
    return Tag.objects.create(
        name=NAME,
        color='color16',
        slug='TestSlug',
        id=MAIN_ID,
    )


@pytest.fixture
def ingredients():
    Ingredient.objects.create(name=NAME, measurement_unit='г', id=MAIN_ID)

    Ingredient.objects.bulk_create(
        Ingredient(
            name=f'XIngTest{i}X', measurement_unit='г', id=MAIN_ID + 1 + i
        )
        for i in range(NEW_OBJECTS_QUANTITY)
    )

    Ingredient.objects.create(
        name='Search',
        measurement_unit='г',
        id=NEW_OBJECTS_QUANTITY + MAIN_ID + 1,
    )
