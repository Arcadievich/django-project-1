from django.contrib import admin
from django.urls import path, include
from where_to_go import views
from places.views import place_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_index),
    path('place/<int:place_id>/', place_json, name='place_details_json'),
    path('tinymce/', include('tinymce.urls')),
]
