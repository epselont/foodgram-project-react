from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
