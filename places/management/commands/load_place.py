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
            place_json = response.json()

            self.load_place(place_json)

        except requests.exceptions.RequestException as e:
            raise CommandError(f'Ошибка при загрузке по URL: {e}')
        except KeyError as e:
            raise CommandError(f'Ошибка в структуре JSON: отсутствует поле {e}')
        except Exception as e:
            raise CommandError(f'Ошибка: {e}')
        
    @transaction.atomic
    def load_place(self, place_json):
        place, created = Place.objects.get_or_create(
            title=place_json['title'],
            defaults={
                'description_short': place_json.get('description_short', ''),
                'description_long': place_json.get('description_long', ''),
                'lat': place_json['coordinates']['lat'],
                'lon': place_json['coordinates']['lng'],
            }
        )

        if not created:
            place.description_short = place_json.get('description_short', '')
            place.description_long = place_json.get('description_long', '')
            place.lat = place_json['coordinates']['lat']
            place.lon = place_json['coordinates']['lng']
            place.save()

        if 'imgs' in place_json:
            self.load_images(place, place_json['imgs'])

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

                image = PlaceImage(place=place, order=order)
                image.image.save(
                    img_name,
                    ContentFile(response.content),
                    save=True
                )
            except requests.exceptions.RequestException:
                continue