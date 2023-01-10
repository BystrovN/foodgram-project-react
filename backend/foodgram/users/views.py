from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import GetTokenSerializer
from .exceptions import PasswordFailedException

User = get_user_model()


class GetTokenView(APIView):
    """
    Представление для получения пользователем токена.
    """

    permission_classes = (AllowAny,)
    serializer_class = GetTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User, email=serializer.validated_data.get('email')
        )

        if user.check_password(serializer.validated_data.get('password')):
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={'token': token.key}, status=HTTPStatus.CREATED
            )

        raise PasswordFailedException


@api_view(['POST'])
def delete_token_view(request):
    """
    Представление для удаления токена пользователя.
    """
    token = get_object_or_404(Token, user_id=request.user.id)
    token.delete()

    return Response(status=HTTPStatus.NO_CONTENT)
