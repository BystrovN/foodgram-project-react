# Generated by Django 4.1.4 on 2023-01-18 17:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0009_alter_recipeingredient_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="amount",
            field=models.SmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1, "Количество ингридиента должно быть больше единицы."
                    )
                ]
            ),
        ),
    ]