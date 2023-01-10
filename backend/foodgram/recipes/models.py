from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from .validators import validate_lowercase

User = get_user_model()
MIN_AMOUNT: int = 0.01


class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'ингридиент'
        verbose_name_plural = 'ингридиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_lowercase,),
    )
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=(validate_lowercase,),
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField()
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tag = models.ManyToManyField(Tag)
    cooking_time = models.SmallIntegerField(
        validators=(
            MinValueValidator(
                1, 'Время приготовления не может быть меньше одной минуты.'
            ),
        )
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(
        validators=(
            MinValueValidator(
                MIN_AMOUNT, 'Количество ингридиентов должно быть больше нуля.'
            ),
        )
    )

    class Meta:
        verbose_name = 'ингридиент к рецепту'
        verbose_name_plural = 'ингридиенты к рецепту'
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} -> {self.ingredient}'


class FavoriteList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'favorites'
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'shopping'
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping',
            )
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'
