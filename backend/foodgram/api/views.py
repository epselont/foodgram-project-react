from recipes.models import Ingredient
from rest_framework import viewsets

from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
