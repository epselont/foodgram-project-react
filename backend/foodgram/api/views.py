from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, SubscribeSerializer, TagSerializer,
                          UserSerializer)

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
        pages = self.paginate_queryset(user.subscribe.all())
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', "DELETE"], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        follow = get_object_or_404(User, id=kwargs.get('id'))
        already_subscribe = user.subscribe.filter(id=follow.id).exists()
        serializer = SubscribeSerializer(follow, context={'request': request})
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
            user.subscribe.add(follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            user.subscribe.remove(follow)
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


# TODO Приступить к Рецептам
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({'author': request.user.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
