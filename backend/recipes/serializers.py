from rest_framework import serializers
from rest_framework import permissions

from recipes.models import Recipe, Tags, RecipeIngredients, Ingredients
from users.serializers import ProfileSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'name', 'slug',)
    

class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    
    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')

class IngredientCreateResipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', queryset=Ingredients.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')

class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = ProfileSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, source='recipeingredients_set')
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('action') not in permissions.SAFE_METHODS:
            self.fields['ingredients'] = IngredientCreateResipeSerializer(many=True, write_only=True)
            self.fields['tags'] = serializers.PrimaryKeyRelatedField(write_only=True, many=True, queryset=Tags.objects.all())
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):
        user = self.context['request'].user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        # validated_data['author'] = user
        # recipe = super().create(validated_data)
        recipe = Recipe.objects.create(author=user, **validated_data)
        # ingredients_serialazers = IngredientCreateResipeSerializer(data=ingredients, many=True)
        # ingredients_serialazers.is_valid(raise_exception=True)
        # ingredients_serialazers.save(recipe=recipe)
        ingredients_list = []
        for ingredient_data in ingredients:
            ingredient = ingredient_data['ingredient']['id']
            amount = ingredient_data['amount']
            recipe_ingredient = RecipeIngredients(ingredient=ingredient, recipe=recipe, amount=amount)
            ingredients_list.append(recipe_ingredient)
        RecipeIngredients.objects.bulk_create(ingredients_list)
        recipe.tags.add(*tags)

        return recipe
    
    def update(self, value, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        value.ingredients.clear()
        # recipe = Recipe.objects.update(**validated_data)
        # ingredients_serializers = IngredientCreateResipeSerializer(data=ingredients, many=True)
        # ingredients_serializers.is_valid(raise_exception=True)
        # ingredients_serializers.save()
        ingredients_list = []
        for ingredient_data in ingredients:
            ingredient = ingredient_data['ingredient']['id']
            amount = ingredient_data['amount']
            recipe_ingredient = RecipeIngredients(ingredient=ingredient, recipe=value, amount=amount)
            ingredients_list.append(recipe_ingredient)
        RecipeIngredients.objects.bulk_create(ingredients_list)
        value.tags.clear()
        value.tags.add(*tags)

        return super().update(value, validated_data)

    def get_is_favorited(self, recipe) -> bool:
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return recipe.lovers.filter(id=request.user.id).exists()
    
    def get_is_in_shopping_cart(self, recipe) -> bool:
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return recipe.buyers.filter(id=request.user.id).exists()



# class CreateRecipeSerializer(serializers.ModelSerializer):
#     ingredients = IngredientCreateResipeSerializer(many=True, write_only=True)

#     class Meta:
#         model = Recipe
#         fields = ('ingredients', 'tags', 'name', 'text', 'image', 'cooking_time',)

#     def create(self, validated_data):
#         user = self.context['request'].user
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         # validated_data['author'] = user
#         # recipe = super().create(validated_data)
#         recipe = Recipe.objects.create(author=user, **validated_data)
#         # ingredients_serialazers = IngredientCreateResipeSerializer(data=ingredients, many=True)
#         # ingredients_serialazers.is_valid(raise_exception=True)
#         # ingredients_serialazers.save(recipe=recipe)
#         # print(ingredients)
#         ingredients_list = []
#         for ingredient_data in ingredients:
#             ingredient = ingredient_data['ingredient']['id']
#             amount = ingredient_data['amount']
#             #print(ingredient.id)
#             recipe_ingredient = RecipeIngredients(ingredient=ingredient, recipe=recipe, amount=amount)
#             ingredients_list.append(recipe_ingredient)
#         RecipeIngredients.objects.bulk_create(ingredients_list)
#         recipe.tags.add(*tags)
#         # print(tags)

#         return recipe
    
#     def update(self, value, validated_data):
#         # user = self.context['request'].user
#         ingredients = validated_data.pop('ingredients')
#         tags = validated_data.pop('tags')
#         value.ingredients.clear()
#         # recipe = Recipe.objects.update(**validated_data)
#         # ingredients_serializers = IngredientCreateResipeSerializer(data=ingredients, many=True)
#         # ingredients_serializers.is_valid(raise_exception=True)
#         # ingredients_serializers.save()
#         ingredients_list = []
#         for ingredient_data in ingredients:
#             ingredient = ingredient_data['ingredient']['id']
#             amount = ingredient_data['amount']
#             #print(ingredient.id)
#             recipe_ingredient = RecipeIngredients(ingredient=ingredient, recipe=value, amount=amount)
#             ingredients_list.append(recipe_ingredient)
#         RecipeIngredients.objects.bulk_create(ingredients_list)
#         value.tags.clear()
#         value.tags.add(*tags)

#         return super().update(value, validated_data)














# .select_related('author')\
#         .only(
#             'name', 'image', 'text', 'cooking_time', 'author__username',
#             'author__first_name', 'author__last_name', 'author__email', 'author__avatar',
#         )\
#         .prefetch_related('tags', 
#                           Prefetch('recipeingredients_set',
#                                    RecipeIngredients.objects.select_related('ingredient')\
#                                     .only('ingredient__measurement_unit', 'ingredient__name', 'ingredient__id', 'recipe__id', 'amount') ))
