from django.contrib import admin
from django.utils.html import format_html
from .models import Place, PlaceImage
from adminsortable2.admin import SortableAdminMixin, SortableTabularInline, SortableAdminBase


class PlaceImageInline(SortableTabularInline):
    model = PlaceImage
    fields = ['image', 'preview', 'order']
    readonly_fields = ['preview']

    def preview(self, obj):
        url = obj.image.url

        return format_html(f'<img src="{url}" style="max-height: 200px;" />')
    
    preview.short_description = 'Превью'


@admin.register(PlaceImage)
class PlaceImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'place', 'image', 'preview', 'order']

    def preview(self, obj):
        url = obj.image.url

        return format_html(f'<img src="{url}" style="max-height: 200px;" />')


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', 'description_short', 'lon', 'lat']
    inlines = [PlaceImageInline]