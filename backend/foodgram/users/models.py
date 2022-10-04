from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models

MAX_LENGTH = 150
MIN_LENGTH = 3
MIN_LENGTH_ERR_MSG = f'Введите не менее {MIN_LENGTH} символов.'


class User(AbstractUser):

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

    email = models.EmailField(
        'Адрес почты',
        max_length=254,
        unique=True
    )

    first_name = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH,
        validators=[
            MinLengthValidator(
                MIN_LENGTH,
                MIN_LENGTH_ERR_MSG
            )
        ]
    )

    last_name = models.CharField(
        'Фамилия пользователя',
        max_length=MAX_LENGTH,
        validators=[
            MinLengthValidator(
                MIN_LENGTH,
                MIN_LENGTH_ERR_MSG
            )
        ]
    )

    follower = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name='Подписка на автора',
        blank=True,
        symmetrical=False
    )

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    @property
    def is_admin(self):
        return self.role == 'ADMIN'

    @property
    def is_user(self):
        return self.role == 'USER'
