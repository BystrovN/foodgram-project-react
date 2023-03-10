# Generated by Django 4.1.4 on 2023-01-13 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0005_recipeingredient_unique_ingredient"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="measurement_unit",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(db_index=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
