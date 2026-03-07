from django.db import models

from tinymce.models import HTMLField


class Place(models.Model):
    """Модель локации для отдыха."""
    title = models.CharField('Название')
    short_description = models.CharField(
        'Короткое описание',
        max_length=300,
        blank=True
    )
    long_description = HTMLField('Длинное описание', blank=True)
    lon = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f'{self.title}'
    

class PlaceImage(models.Model):
    """Модель для картинок локаций."""
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='static/images/'
    )
    order = models.PositiveIntegerField(
        'Порядок сортировки',
        default=1,
        help_text='Чем число меньше, тем выше в списке',
    )

    class Meta:
        verbose_name = 'Фотография локации'
        verbose_name_plural = 'Фотографии локации'
        ordering = ['order']
        indexes = [
            models.Index(fields=['order'], name='placeimage_order_index')
        ]

    def __str__(self):
        return f'{self.order} - {self.place.title}'