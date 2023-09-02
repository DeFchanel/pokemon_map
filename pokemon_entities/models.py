from django.db import models  # noqa F401
import datetime


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название покемона', max_length=200)
    image = models.ImageField(
        verbose_name='Картинка покемона',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание покемона',
        blank=True
    )
    title_jp = models.CharField(
        verbose_name='Японское название покемона',
        max_length=200,
        blank=True
    )
    title_en = models.CharField(
        verbose_name='Английское название покемона',
        max_length=200,
        blank=True
    )
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Прошлая эволюция покемона',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Что за покемон',
        on_delete=models.CASCADE,
        related_name='entities'
    )
    lat = models.FloatField(verbose_name='Географическая ширина')
    lon = models.FloatField(verbose_name='Географическая высота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Стамина')

    def __str__(self):
        return self.pokemon.title
