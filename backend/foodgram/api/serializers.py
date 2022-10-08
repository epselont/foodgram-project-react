from ast import In

from pyexpat import model
from recipes.models import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')
