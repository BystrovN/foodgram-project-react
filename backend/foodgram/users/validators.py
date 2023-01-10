from rest_framework.exceptions import ValidationError


def validate_username(username: str) -> None:
    if username == 'me':
        raise ValidationError('имя "me" запрещено')
