import json
from django.core.management.base import BaseCommand
from map.models import ISO_CODES
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Load country data from JSON file into the database'
    
    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'iso_code.json')
        with open(file_path, 'r') as file:
            country_data = json.load(file)

            for iso_code, name in country_data.items():
                ISO_CODES.objects.get_or_create(iso_code=iso_code, name=name)
                self.stdout.write(self.style.SUCCESS(f'Successfully added {name}'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded country data'))