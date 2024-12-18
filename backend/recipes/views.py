from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Prefetch
#from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from logging import getLogger

from recipes.models import Recipe, Ingredients, Tags, RecipeIngredients
from users.models import Profile
from recipes.serializers import RecipesSerializer, IngredientSerializer, TagSerializer  # , CreateRecipeSerializer
from recipes.permissions import IsAuthor
from recipes.pagination import RecipePagination


logger = getLogger('recipes')


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author')\
        .only(
            'name', 'image', 'text', 'cooking_time', 'author__username',
            'author__first_name', 'author__last_name', 'author__email', 'author__avatar',
        )\
        .prefetch_related('tags', 
                          Prefetch('recipeingredients_set',
                                   RecipeIngredients.objects.select_related('ingredient')\
                                    .only('ingredient__measurement_unit', 'ingredient__name', 'ingredient__id', 'recipe__id', 'amount') ))
    pagination_class = RecipePagination
    serializer_class = RecipesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthor,)

    # def get_serializer_class(self):
    #     if self.action in ('create', 'update'):
    #         return CreateRecipeSerializer
# 
        # return RecipesSerializer
    
    def get_serializer_context(self):
        
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

    def create(self, request):
        self.perform_create
        try:
            responce = super().create(request)

            id = responce.data['id']
            logger.info(f'Пользователь {request.user.id} добавил рецепт {id}')
            return responce
        except ValidationError as error:
            logger.error(f'Пользователь {request.user.id} пытался добавить рецепт данными {request.data}, произошла ошибка: {error}.')
            raise error
    


    # def create(self, request):
    #     input_serializer_class = self.get_serializer_class()
    #     input_serializer = input_serializer_class(data=request.data, context=self.get_serializer_context())
    #     if input_serializer.is_valid():
    #         recipe = input_serializer.save()
    #         output_serializer = RecipesSerializer(recipe, context=self.get_serializer_context())
    #     else:
    #         return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(output_serializer.data)
    
    # def update(self, request, pk):
    #     recipe = self.get_object()
    #     input_serializer_class = self.get_serializer_class()
    #     input_serializer = input_serializer_class(data=request.data, instance=recipe, context=self.get_serializer_context())
    #     if input_serializer.is_valid():
    #         recipe = input_serializer.save()
    #         output_serializer = RecipesSerializer(recipe, context=self.get_serializer_context())
    #     else:
    #         return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response(output_serializer.data)

class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

