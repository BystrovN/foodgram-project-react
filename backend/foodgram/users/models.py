from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from .validators import validate_username


class CustomUser(AbstractUser):

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(), validate_username),
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.username
