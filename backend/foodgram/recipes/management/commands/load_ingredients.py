import json

from django.core.management import BaseCommand
from recipes.models import Ingredients

ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить данные из json-файла,
сначала очистите БД.
"""


class Command(BaseCommand):
    help = "Загрузка данных"

    def handle(self, *args, **options):

        if Ingredients.objects.exists():
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        with open('../../data/ingredients.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for dict in data:
                Ingredients.objects.create(
                    name=dict['name'], measurement_unit=dict['measurement_unit'])
            print("Данные загружены")
