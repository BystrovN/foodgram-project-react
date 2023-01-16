def is_favorited(user, recipe_id):
    """Проверяем добавлен ли рецепт у пользователя в избранное."""
    return (
        user.is_authenticated
        and user.favorites.filter(recipe_id=recipe_id).exists()
    )


def is_in_shopping_cart(user, recipe_id):
    """Проверяем добавлен ли рецепт у пользователя в корзину."""
    return (
        user.is_authenticated
        and user.shopping.filter(recipe_id=recipe_id).exists()
    )
