from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserViewSet
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, SubscribeReceptSerializer,
                          SubscribeSerializer, TagSerializer, UserSerializer)

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
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in [
            'create', 'shopping_cart', 'favorite', 'download_shopping_cart'
        ]:
            self.permission_classes = [IsAuthenticated, ]
        elif self.action == ['update', 'destroy']:
            self.permission_classes = [IsAdminOrAuthorOrReadOnly, ]
        else:
            self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST', "DELETE"], detail=True)
    def favorite(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
        if request.method == 'POST':
            serializer = SubscribeReceptSerializer(
                recipe, context={'request': request}
            )
            request.user.favorites.add(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            request.user.favorites.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', "DELETE"], detail=True)
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
        if request.method == 'POST':
            serializer = SubscribeReceptSerializer(
                recipe, context={'request': request}
            )
            request.user.shop_list.add(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            request.user.shop_list.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = user.shop_list.all().values_list(
            'ingredients__name',
            'ingredients__measurement_unit'
        ).annotate(Sum('ingredients_recipe__amount'))
        shop_list = ("Список покупок: \n\n")
        for ingredient in ingredients:
            shop_list += (
                f'{ingredient[0].capitalize()} '
                f'({ingredient[1]}) - '
                f'{ingredient[2]}\n'
            )
        file_name = f'{user.email}_shop_list'
        response = HttpResponse(
            shop_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = (
            f'attachment; filename={file_name}.txt'
        )
        return response
