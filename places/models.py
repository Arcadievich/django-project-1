from django.db import models


class Place(models.Model):
    """Модель локации для отдыха."""
    title = models.CharField('Название')
    description_short = models.TextField(
        'Короткое описание',
        max_length=300,
    )
    description_long = models.TextField('Длинное описание')
    lon = models.FloatField('Долгота')
    lat = models.FloatField('Широта')

    def __str__(self):
        return f'{self.title}'