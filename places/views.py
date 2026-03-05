from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from places.models import Place


def place_json(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related('images'), id=place_id)

    imgs = [image.image.url for image in place.images.all()]

    place_details = {
        'title': place.title,
        'imgs': imgs,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lon,
        },
    }

    params = {
        'ensure_ascii': False,
        'indent': 2,
    }

    return JsonResponse(place_details, json_dumps_params=params)

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
                'detailsUrl': reverse('place_details_json', args=[place.id]),
            },
        }
        features.append(feature)

    places_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    return render(request, 'index.html', {'places_geojson': places_geojson})