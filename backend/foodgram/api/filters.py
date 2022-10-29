from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(method='filter_shopping_cart')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('author', 'is_in_shopping_cart', 'is_favorited', 'tags')

    def filter_shopping_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(shop_list=self.request.user)
        elif value == 0:
            return queryset.exclude(shop_list=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favorite=self.request.user)
        elif value == 0:
            return queryset.exclude(favorite=self.request.user)
        return queryset
