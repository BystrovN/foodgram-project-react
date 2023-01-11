from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination

from . import serializers
from .exceptions import PasswordFailedException
from .mixins import ListCreateRetrieveModelMixin

User = get_user_model()


class GetTokenView(APIView):
    """
    Представление для получения пользователем токена.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, email=serializer.validated_data.get('email')
        )

        if user.check_password(serializer.validated_data.get('password')):
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={'token': token.key}, status=status.HTTP_201_CREATED
            )

        raise PasswordFailedException


@api_view(['POST'])
def delete_token_view(request):
    """
    Представление для удаления токена пользователя.
    """
    token = get_object_or_404(Token, user_id=request.user.id)
    token.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(ListCreateRetrieveModelMixin):
    """
    Представление для вывода списка и создания экземпляра пользователя.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.UserListSerializer

        return serializers.UserInstanceSerializer


class UserMeView(APIView):
    """
    Представление для просмотра информации о себе.
    """

    serializer_class = serializers.UserListSerializer

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
