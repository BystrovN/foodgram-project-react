# Generated by Django 4.1.4 on 2023-01-11 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_customuser_email"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "ordering": ("id",),
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
            },
        ),
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(max_length=150),
        ),
    ]