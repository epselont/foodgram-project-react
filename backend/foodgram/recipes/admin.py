from django.contrib import admin

from .models import Ingredient, IngredientsRecipe, Recipe, Tag


@admin.register(Ingredient)
class AdminIngredients(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('color',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = ('name', 'author', 'text', 'cooking_time', 'favorite_count')
    raw_id_fields = ('author', 'tags')
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('name', 'tags')
    empty_value_display = '-пусто-'

    def favorite_count(self, obj):
        return obj.favorite.count()


@admin.register(IngredientsRecipe)
class AdminIngredintsRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = '-пусто-'
