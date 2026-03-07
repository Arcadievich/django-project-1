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

        return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', url)
    
    preview.short_description = 'Превью'


@admin.register(PlaceImage)
class PlaceImageAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'place', 'image', 'preview', 'order']
    raw_id_fields = ['place']

    def preview(self, obj):
        url = obj.image.url

        return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', url)


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title', 'short_description', 'lon', 'lat']
    inlines = [PlaceImageInline]

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }