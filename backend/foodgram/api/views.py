from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag
from rest_framework import status, viewsets
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
        if self.action in ['me', 'subscriptions', 'subscribe']:
            self.permission_classes = [IsAuthenticated, ]
        elif self.action == 'GET':
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        user = request.user
        following = user.follower.all()
        serializer = UserSerializer(
            following, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['POST', "DELETE"], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        follow = get_object_or_404(User, id=kwargs.get('id'))
        already_subscribe = user.follower.filter(id=follow.id).exists()
        serializer = UserSerializer(follow, context={'request': request})
        if user == follow or (
            request.method == 'DELETE' and not already_subscribe
        ):
            return Response(
                {
                    'errors': 'Данное действие не поддерживается!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'POST':
            if already_subscribe:
                return Response(
                    {
                        'errors': 'Вы уже подписаны на этого пользователя!'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.follower.add(follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user.follower.remove(follow)
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# TODO Приступить к Рецептам
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
