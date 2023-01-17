def is_favorited(request, recipe_id):
    """Проверяем добавлен ли рецепт у пользователя в избранное."""
    if not request:
        return False
    return (
        request.user.is_authenticated
        and request.user.favorites.filter(recipe_id=recipe_id).exists()
    )


def is_in_shopping_cart(request, recipe_id):
    """Проверяем добавлен ли рецепт у пользователя в корзину."""
    if not request:
        return False
    return (
        request.user.is_authenticated
        and request.user.shopping.filter(recipe_id=recipe_id).exists()
    )
