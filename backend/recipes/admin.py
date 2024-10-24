from django.contrib import admin

from recipes.models import Recipe, Ingredients, Tags, RecipeIngredients


class RecipeIngredientsAdmin(admin.StackedInline):
    model = RecipeIngredients


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsAdmin,]


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass

