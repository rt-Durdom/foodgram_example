from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (RecipesViewSet, IngredientsViewSet, TagsViewSet)
from users.views import ProfileViewSet


namespace = 'recipes'

router = DefaultRouter()
router.register(r'recipes', RecipesViewSet, basename='recipes'),
router.register(r'ingredients', IngredientsViewSet, basename='ingredients'),
router.register(r'tags', TagsViewSet, basename='tags'),
# router.register(r'users', ProfileViewSet, basename='profile'),

urlpatterns = [
    path('', include(router.urls)),
    # path('auth')
]
