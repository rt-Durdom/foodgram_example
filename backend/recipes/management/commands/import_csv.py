import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        try:
            with open(
                f'{settings.BASE_DIR}/data/ingredients.csv',
                'r',
                encoding='utf-8',
            ) as ingred:
                ingredient_reader = csv.reader(ingred)
                Ingredients.objects.all().delete()
                Ingredients.objects.bulk_create(
                    Ingredients(
                        name=row[0],
                        measurement_unit=row[1])
                    for row in ingredient_reader)
        except FileNotFoundError:
            raise TypeError('Файл не найден!')
        self.stdout.write(self.style.SUCCESS('Файл успешно загружен!'))
