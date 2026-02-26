from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    """Модель локации для отдыха."""
    title = models.CharField('Название')
    description_short = models.TextField(
        'Короткое описание',
        max_length=300,
    )
    description_long = HTMLField('Длинное описание')
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

    def __str__(self):
        return f'{self.order} - {self.place.title}'