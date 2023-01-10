def is_subscribed(user, author):
    """Проверяем подписан ли пользователь на автора."""
    return (
        user.is_authenticated and user.follower.filter(author=author).exists()
    )
