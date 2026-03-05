from django.contrib import admin
from django.urls import path, include

from places.views import place_json, show_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_index),
    path('place/<int:place_id>/', place_json, name='place_details_json'),
    path('tinymce/', include('tinymce.urls')),
]
