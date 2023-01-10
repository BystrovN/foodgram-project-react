# Generated by Django 4.1.4 on 2023-01-09 16:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=150, unique=True)),
                ("measurement_unit", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "ингридиент",
                "verbose_name_plural": "ингридиенты",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("image", models.ImageField(upload_to="recipes/")),
                ("text", models.TextField()),
                (
                    "cooking_time",
                    models.SmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                1,
                                "Время приготовления не может быть меньше одной минуты.",
                            )
                        ]
                    ),
                ),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "рецепт",
                "verbose_name_plural": "рецепты",
                "ordering": ("-pub_date",),
                "default_related_name": "recipes",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        validators=[recipes.validators.validate_lowercase],
                    ),
                ),
                ("color", models.CharField(max_length=7, unique=True)),
                (
                    "slug",
                    models.SlugField(
                        unique=True, validators=[recipes.validators.validate_lowercase]
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ShoppingList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipes.recipe"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "список покупок",
                "verbose_name_plural": "список покупок",
                "ordering": ("user",),
                "default_related_name": "shopping",
            },
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(
                                0, "Количество ингридиентов должно быть больше нуля."
                            )
                        ]
                    ),
                ),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recipes.ingredient",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipes.recipe"
                    ),
                ),
            ],
            options={
                "verbose_name": "ингридиент к рецепту",
                "verbose_name_plural": "ингридиенты к рецепту",
                "ordering": ("recipe",),
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredient",
            field=models.ManyToManyField(
                through="recipes.RecipeIngredient", to="recipes.ingredient"
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tag",
            field=models.ManyToManyField(to="recipes.tag"),
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="follower",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "подписка",
                "verbose_name_plural": "подписки",
                "ordering": ("user",),
            },
        ),
        migrations.CreateModel(
            name="FavoriteList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="recipes.recipe"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "избранное",
                "verbose_name_plural": "избранное",
                "ordering": ("user",),
                "default_related_name": "favorites",
            },
        ),
        migrations.AddConstraint(
            model_name="follow",
            constraint=models.UniqueConstraint(
                fields=("user", "author"), name="unique_follower"
            ),
        ),
    ]
