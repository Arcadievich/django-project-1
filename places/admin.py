from django.contrib import admin
from django.utils.html import format_html
from .models import Place, PlaceImage


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    fields = ['image', 'preview', 'order']
    readonly_fields = ['preview']

    def preview(self, obj):
        url = obj.image.url

        return format_html(f'<img src="{url}" style="max-height: 200px;" />')
    
    preview.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PlaceImageInline]