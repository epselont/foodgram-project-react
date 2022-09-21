from django.contrib import admin

from .models import Ingredients


@admin.register(Ingredients)
class AdminIngredients(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'
