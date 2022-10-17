from django.contrib.auth import get_user_model
from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag
from rest_framework import serializers

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredients.id')
    name = serializers.CharField(source='ingredients.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientsRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsRecipeSerializer(
        source='ingredients_recipe',
        read_only=True,
        many=True,
    )

    class Meta:
        model = Recipe
        exclude = ['favorite', 'shop_list', 'pub_date']

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def get_is_in_shoping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.shop_list.filter(id=obj.id).exists()
