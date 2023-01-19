import pytest
from django.core import management

from recipes.models import Ingredient

INGREDIENT_QUANTITY_IN_FILE = 2188


@pytest.mark.django_db(transaction=True)
def test_00_csv_import_ingredients():
    assert len(Ingredient.objects.all()) == 0

    management.call_command('csv_ingredients_import')

    assert (
        len(Ingredient.objects.all()) == INGREDIENT_QUANTITY_IN_FILE
    )
