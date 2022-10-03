from django.contrib import admin

from .models import Ingredient, IngredientsRecipe, Recipe, Tag


@admin.register(Ingredient)
class AdminIngredients(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('color',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = ('pk', 'name', 'text', 'cooking_time',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(IngredientsRecipe)
class AdminIngredintsRecipe(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredients', 'amount')
