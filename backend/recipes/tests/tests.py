import pytest
import json
from pathlib import Path
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse, reverse_lazy

from recipes.models import Recipe, Ingredients, Tags, RecipeIngredients
from users.models import Profile



@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def required_recipes_data():
    path_file = Path(__file__).parent / 'test_list_recipe.json'
    with open(path_file, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    return data


@pytest.mark.django_db
def test_list_recipe(api_client, required_recipes_data):
    user = Profile.objects.create_user(username='username', password='12345')
    ingredient1 = Ingredients.objects.create(name='name', measurement_unit='г')
    ingredient2 = Ingredients.objects.create(name='name2', measurement_unit='г')
    tag1 = Tags.objects.create(name='name', slug='slug')
    tag2 = Tags.objects.create(name='name2', slug='slug2')

    recipe1 = Recipe.objects.create(
        name='luk',
        author=user,
        text='models.TextField()',
        cooking_time=1,
    )
    recipe2 = Recipe.objects.create(
        name='luk2',
        author=user,
        text='models.TextField()',
        cooking_time=10,
    )
    RecipeIngredients.objects.create(recipe=recipe1, ingredient=ingredient1, amount=20)
    RecipeIngredients.objects.create(recipe=recipe2, ingredient=ingredient2, amount=200)
    RecipeIngredients.objects.create(recipe=recipe2, ingredient=ingredient2, amount=10)

    recipe1.tags.add(tag1, tag2)
    recipe2.tags.add(tag2)

    url = reverse('recipes-list')

    responce = api_client.get(url)
    print(responce.json())
    data = responce.json()

    # pytest - documentation
    assert responce.status_code == status.HTTP_200_OK
    assert len(data) == 2
    assert data[0]['name'] == 'luk'
    assert data[1]['name'] == 'luk2'
    assert len(data[0]['ingredients']) == 1
    assert len(data[1]['ingredients']) == 2
    assert len(data[0]['tags']) == 2
    assert len(data[1]['tags']) == 1
    assert data == required_recipes_data
    #assert data[0]['tags'] == 1
