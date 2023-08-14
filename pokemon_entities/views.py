import folium
import json
from dateutil.tz import *
from django.utils.timezone import now, localtime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from dateutil import tz

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = localtime(now(), tz.gettz('UTC'))
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=time_now, disappeared_at__gte=time_now)
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.image:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )
        else:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                None
            )
    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': None,
                'title_ru': pokemon.title
            })  

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=int(pokemon_id))
    requested_pokemon = pokemon

    pokemon = {
        "pokemon_id": int(pokemon_id),
        "title_ru": requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "description": requested_pokemon.description,
        "img_url": request.build_absolute_uri(requested_pokemon.image.url),
    }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = localtime(now(), tz.gettz('UTC'))
    pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon, appeared_at__lte=time_now, disappeared_at__gte=time_now)
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.image:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )
        else:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                None
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
