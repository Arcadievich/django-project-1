from django.shortcuts import render
from places.models import Place, PlaceImage
import json


def show_index(request):
    places = Place.objects.all()

    features = []
    for place in places:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lon, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': str(place.id),
                'detailsUrl': f'static/places/{place.id}.json'
            }
        }
        features.append(feature)

    places_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    places_json = json.dumps(places_geojson, ensure_ascii=False)

    return render(request, 'index.html', {'places_geojson': places_json})