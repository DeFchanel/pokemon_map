from django.db import models  # noqa F401
import datetime
class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='next_evolution'
    )
    

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=datetime.datetime.now())
    disappeared_at = models.DateTimeField(default=datetime.datetime.now())
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    strength = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.pokemon.title)