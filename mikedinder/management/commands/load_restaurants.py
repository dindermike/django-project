import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from pathlib import Path

from mikedinder.models import Restaurant


class Command(BaseCommand):
    """
    Command to Load the CSV Dataset Provided for this Exercise.

    Usage (Without Quotation Marks): "python manage.py load_restaurants --path app/raw_data/restaurants.csv"
    """
    help = 'Load Restaurants from a Specified CSV File Path'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='The Path to the Restaurants CSV File')

    def handle(self, *args, **kwargs):
        base_dir = Path(settings.BASE_DIR)
        print(kwargs['path'])
        file_path = base_dir / kwargs['path']

        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip the Header Row if it Exists
            restaurants = []

            for row in reader:
                try:
                    restaurant = Restaurant(
                        name=row[0],
                        hours=row[1]
                    )
                    restaurants.append(restaurant)
                except (ValueError, IndexError) as e:
                    self.stdout.write(self.style.ERROR(f'Error Processing Row: {row} - {e}'))

            # Use bulk_create for Faster Insertion
            Restaurant.objects.bulk_create(restaurants)

            self.stdout.write(self.style.SUCCESS('Data Successfully Imported'))
