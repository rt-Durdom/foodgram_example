from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from users.models import Profile

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'j', 'з': 'z', 'и': 'i',
            'й': 'iy', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

def auto_slugify(s):
    return slugify(''.join(alphabet.get(w, w) for w in s.lower()))

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(max_length=150, unique=True)
    measurement_unit = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )
    image = models.ImageField(null=True, blank=True)
    tags = models.ManyToManyField(Tags,)
    ingredients = models.ManyToManyField(Ingredients, through='RecipeIngredients')
    buyers = models.ManyToManyField(Profile, related_name='purchases', blank=True)
    lovers = models.ManyToManyField(Profile, related_name='favorites', blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug_set = set(Recipe.objects.values_list('slug', flat=True))
        self.slug = auto_slugify(self.name)
        if self.slug in slug_set:
            self.slug += '_' + str(self.id)
        super().save(*args, **kwargs)



class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.PROTECT)
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'
