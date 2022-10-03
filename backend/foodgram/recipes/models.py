from email import message
from unicodedata import name

from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator, RegexValidator,
                                    int_list_validator)
from django.db import models

MAX_LENGTH = 200
MIN_LENGTH = 3
MIN_LENGTH_ERR_MSG = f'Введите не менее {MIN_LENGTH} символов.'


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=MAX_LENGTH,
        help_text=f'Название ингредиента, не менее {MIN_LENGTH} символов.',
        validators=[
            MinLengthValidator(
                MIN_LENGTH,
                MIN_LENGTH_ERR_MSG
            )
        ]
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LENGTH,
        help_text='Обозначение единицы измерения, не менее 1-го символа.',
        validators=[
            MinLengthValidator(
                1,
                'Введите не менее 1-го символа.'
            )
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(
        'Название тэга',
        max_length=MAX_LENGTH,
        unique=True,
        validators=[
            MinLengthValidator(
                MIN_LENGTH,
                MIN_LENGTH_ERR_MSG
            )
        ]
    )
    color = models.CharField(
        'Цвет в формате HEX',
        max_length=7,
        default='#FFFFFF',
        unique=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})$',
                'Используйте цифры и латинские символы: a-f и A-F. Пример: #A123FFA'
            )
        ]
    )
    slug = models.SlugField(
        'Уникальный слаг тэга',
        max_length=MAX_LENGTH,
        unique=True,
        validators=[
            MinLengthValidator(
                MIN_LENGTH,
                MIN_LENGTH_ERR_MSG
            )
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe'
    )
    tags = models.ManyToManyField(Tag)
    name = models.CharField(
        'Название рецепта',
        max_length=MAX_LENGTH,
    )
    text = models.TextField(
        'Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientsRecipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='ingredients_recipe',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredients_recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=1,
        validators=[
            MinValueValidator(
                1,
                'Введите значение больше 1'
            ),
            MaxValueValidator(
                20000,
                'Введите значение меньше 20000'
            ),
        ]
    )

    def __str__(self):
        return self.ingredients

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ['recipe', ]
