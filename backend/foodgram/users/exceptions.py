from rest_framework.exceptions import AuthenticationFailed


class PasswordFailedException(AuthenticationFailed):
    default_detail = 'Неверный пароль.'
