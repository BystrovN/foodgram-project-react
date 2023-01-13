from rest_framework.exceptions import APIException
from rest_framework import status


class PasswordFailedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Неверный пароль.'


class SubscribeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
