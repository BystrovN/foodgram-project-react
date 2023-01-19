import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from recipes.models import Tag, Ingredient, Recipe, FavoriteList, ShoppingList

USER_PASSWORD = '12345'
USER_EMAIL = 'testuser@gmail.com'
NAME = 'TestTestTest'
MAIN_ID = 1
NEW_OBJECTS_QUANTITY = 3
IMAGE = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABiey'
    'waAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACk'
    'lEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=='
)


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
def second_user(django_user_model):
    return django_user_model.objects.create_user(
        username='Second',
        password=USER_PASSWORD,
        email='secondtestuser@gmail.com',
        first_name='Second',
        last_name='User',
        id=MAIN_ID + 1,
    )


@pytest.fixture
def second_user_client(second_user):
    token = Token.objects.create(user=second_user)
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
def second_tag():
    return Tag.objects.create(
        name='second_tag',
        color='color10',
        slug='second_tag',
        id=MAIN_ID + 1,
    )


@pytest.fixture
def five_ingredients():
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


@pytest.fixture
def recipe(user):
    return Recipe.objects.create(
        author=user,
        name='TestRecipe',
        image=IMAGE,
        text='TestText',
        cooking_time=1,
        id=MAIN_ID,
    )


@pytest.fixture
def fav_recipe(user, recipe):
    return FavoriteList.objects.create(user=user, recipe=recipe, id=MAIN_ID)


@pytest.fixture
def shop_recipe(user, recipe):
    return ShoppingList.objects.create(user=user, recipe=recipe, id=MAIN_ID)
