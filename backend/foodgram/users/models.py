from email.policy import default
from random import choices

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator, RegexValidator)
from django.db import models


class User(AbstractUser):
    MAX_LENGTH = 150
    MIN_LENGTH = 3
    MIN_LENGTH_ERR_MSG = f'Введите не менее {MIN_LENGTH} символов.'

    ROLES = [
        ('ADMIN', 'Администратор'),
        ('USER', 'Пользователь')
    ]

    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLES,
        default='USER'
    )

    username = models.CharField(
        'Логин',
        max_length=MAX_LENGTH,
        unique=True,
        validators=[
            MinLengthValidator(
                MIN_LENGTH,
                MIN_LENGTH_ERR_MSG
            ),
            RegexValidator(
                '^[\w.@+-]+\Z',
                'Можно использовать русские или латинские символы, числа, знаки: "." и "@"'
            )
        ]
    )
