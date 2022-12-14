from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag
from users.models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(DjoserUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.subscribe.filter(id=obj.id).exists()
        )


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
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
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsRecipeSerializer(
        source='ingredients_recipe',
        read_only=True,
        many=True
    )

    class Meta:
        model = Recipe
        exclude = ('favorite', 'shop_list', 'pub_date')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorites.filter(id=obj.id).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.shop_list.filter(id=obj.id).exists()
        )


class RecipeCreateSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientsRecipeSerializer(
        source='ingredients_recipe',
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('favorite', 'shop_list', 'pub_date')
        read_only_fields = ('author', )

    def ingredients_create(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientsRecipe.objects.get_or_create(
                ingredient_id=ingredient['ingredient']['id'],
                recipe=recipe,
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_recipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.ingredients_create(
            ingredients=ingredients,
            recipe=recipe
        )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients_recipe')
        instance.ingredients.clear()
        self.ingredients_create(
            ingredients=ingredients,
            recipe=instance
        )
        return super().update(instance, validated_data)

    def validate(self, data):
        ingredients = data.get('ingredients_recipe')
        tags = data.get('tags')
        if not ingredients:
            raise serializers.ValidationError(
                {
                    'ingredients': '???????????????? ???? ?????????? 1-???? ??????????????????????'
                }
            )
        if not tags:
            raise serializers.ValidationError(
                {
                    'ingredients': '???????????????? ???? ?????????? 1-???? ????????'
                }
            )
        return data


class SubscribeReceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        serializer = SubscribeReceptSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
