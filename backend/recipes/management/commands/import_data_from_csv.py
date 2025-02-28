import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from recipes.models import Ingredient

MODEL_FILES = {
    Ingredient: 'ingredients.csv',
}


class Command(BaseCommand):
    """Management-команда для импорта данных в БД из CSV-файлов."""

    help = 'Импорт данных из CSV-файлов в базу данных'

    def handle(self, *args, **options):
        for model, file_name in MODEL_FILES.items():
            file_path = os.path.join(settings.CSV_FILES_DIR, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    for row in reader:
                        name, measurement_unit = row
                        try:
                            model.objects.create(
                                name=name, measurement_unit=measurement_unit
                            )
                        except IntegrityError:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Ингредиент '{name}' уже существует."
                                )
                            )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Данные из файла {file_name} успешно загружены в БД.'
                    )
                )
            except FileNotFoundError:
                self.stdout.write(
                    self.style.ERROR(
                        f'Файл {file_name} не найден в директории '
                        f'{settings.CSV_FILES_DIR}.'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Произошла ошибка при обработке файла {file_name}: '
                        f'{str(e)}'
                    )
                )
