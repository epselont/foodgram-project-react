from multiprocessing import context

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(DjoserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == ('me' or 'subscriptions' or 'subscribe'):
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        user = request.user
        data = user.follower.all()
        serializer = UserSerializer(
            data, many=True, context={'request': request})
        return Response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
