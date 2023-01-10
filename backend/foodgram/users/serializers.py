from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения пользователем JWT-токена."""

    class Meta:
        model = User
        fields = ('password', 'email')
