from django.contrib.auth import get_user_model

from rest_framework import serializers

from .utils import is_subscribed

User = get_user_model()
IS_SUBSCRIBED_KEY = 'is_subscribed'


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
            IS_SUBSCRIBED_KEY,
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False  # Если пользователь переходит на api/users/me/

        return is_subscribed(request.user, obj)


class UserInstanceSerializer(serializers.ModelSerializer):
    """Сериалайзер экземпляра пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
