from django.contrib.auth import get_user_model

from rest_framework import serializers

from .utils import is_subscribed

User = get_user_model()


class GetTokenSerializer(serializers.Serializer):
    """Сериалайзер для получения пользователем JWT-токена."""

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(
        max_length=128, required=True, write_only=True
    )


class UserListSerializer(serializers.ModelSerializer):
    """Сериалайзер просмотра списка пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return is_subscribed(self.context.get('request').user, obj)


class UserInstanceSerializer(serializers.ModelSerializer):
    """Сериалайзер экземпляра пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
