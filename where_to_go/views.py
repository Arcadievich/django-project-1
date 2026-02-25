from django.shortcuts import render, get_object_or_404
from places.models import Place
import json


def show_index(request):
    places = Place.objects.prefetch_related('images').all()

    features = []
    for place in places:
        images_url = [image.image.url for image in place.images.all()]

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lon, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': str(place.id),
                'imgs': images_url,
                'description_short': place.description_short,
                'description_long': place.description_long,
                'detailsUrl': f'static/places/1.json',
            },
        }
        features.append(feature)

    places_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    places_json = json.dumps(places_geojson, ensure_ascii=False)

    return render(request, 'index.html', {'places_geojson': places_json})