from django.contrib.auth import get_user_model
from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag
from rest_framework import viewsets

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSerializer)

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
