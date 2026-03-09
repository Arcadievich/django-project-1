import requests

from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.db import transaction

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Загружает локацию из JSON файла по URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL JSON файла с данными')

    def handle(self, *args, **options):
        url = options['url']

        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_place = response.json()

            self.load_place(raw_place)

        except requests.exceptions.RequestException as e:
            raise CommandError(f'Ошибка при загрузке по URL: {e}')
        except KeyError as e:
            raise CommandError(f'Ошибка в структуре JSON: отсутствует поле {e}')
        except Exception as e:
            raise CommandError(f'Ошибка: {e}')
        
    @transaction.atomic
    def load_place(self, raw_place):
        place, created = Place.objects.update_or_create(
            title=raw_place['title'],
            defaults={
                'description_short': raw_place.get('description_short', ''),
                'description_long': raw_place.get('description_long', ''),
                'lat': raw_place['coordinates']['lat'],
                'lon': raw_place['coordinates']['lng'],
            }
        )

        if 'imgs' in raw_place:
            self.load_images(place, raw_place['imgs'])

    def load_images(self, place, image_urls):
        existing_images = PlaceImage.objects.filter(place=place)
        existing_urls = set()

        for img in existing_images:
            existing_urls.add(img.image.name)

        for order, img_url in enumerate(image_urls, start=1):
            img_name = img_url.split('/')[-1].split('?')[0]

            if any(img_name in url for url in existing_urls):
                continue

            try:
                response = requests.get(img_url, stream=True)
                response.raise_for_status()

                image = PlaceImage.objects.create(
                    place=place,
                    order=order,
                    image=ContentFile(response.content, name=img_name)
                )
            except requests.exceptions.RequestException:
                continue