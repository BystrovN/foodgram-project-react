from rest_framework.exceptions import APIException
from rest_framework import status


class FavoriteException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class ShoppingCartException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
