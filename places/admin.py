from django.contrib import admin
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PlaceImageInline]