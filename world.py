from random import choice, randint
from poketypes import *
import pygame

WORLD_W = 800
WORLD_H = 600
WORLD_SPRITE_SIZE = 200
WORLD_POKEMON_COUNT = 20


class World:
    def __init__(self):
        self.w = WORLD_W
        self.h = WORLD_H
        self.sprite_size = WORLD_SPRITE_SIZE
        self.max_pokemon = WORLD_POKEMON_COUNT
        self.pokemon = pygame.sprite.Group()
        self.rect = pygame.Rect(0, 0, WORLD_W, WORLD_H)
        self.generate_pokemon()

    def generate_pokemon(self):
        for i in range(self.max_pokemon):
            poketype = choice(FirePokemon, GrassPokemon,
                              WaterPokemon, ElectricPokemon)
            name = choice("Beacross", "Elesaur", "Salamoth", "Penguzz", "Steelzelle", "Slowmeleon", "Ironopotamus", "Bellosaur", "Potatoad",
                          "Scorpike", "Chimpaly", "Barrapod", "Dracung", "Hyenaring", "Hypepion", "Horromite", "Hyparos", "Magicacle", "Flyte", "Manateeth")
            self.pokemon.add(poketype(name, randint(5, 20), randint(5, 20), randint(
                0, WORLD_W - WORLD_SPRITE_SIZE), randint(0, WORLD_H - WORLD_SPRITE_SIZE)))

    def draw(self, surface):
        surface.set_clip(self.rect)
        self.pokemon.draw(surface)

    def update(self):
        for pokemon in self.pokemon.sprites():
            if (pokemon.x <= 0):
                pokemon.vx = abs(pokemon.vx)
            if (pokemon.y <= 0):
                pokemon.vy = abs(pokemon.vy)
            if (pokemon.x >= WORLD_W - WORLD_SPRITE_SIZE):
                pokemon.vx = -abs(pokemon.vx)
            if (pokemon.y >= WORLD_H - WORLD_SPRITE_SIZE):
                pokemon.vy = -abs(pokemon.vy)
