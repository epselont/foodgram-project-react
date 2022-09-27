from django.core.validators import validate_slug
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
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
        max_length=200,
        unique=True
    )
    color = models.CharField(
        'Цвет в формате HEX',
        max_length=7,
        default='#FFFFFF',
        unique=True
    )
    slug = models.SlugField(
        'Уникальный слаг тэга',
        max_length=200,
        unique=True
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
        max_length=200,
    )
    text = models.TextField(
        'Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=0
    )


class IngredientsRecipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=0
    )
