from random import choice, randint
from poketypes import *
import pygame
from properties import *

WORLD_W = props["width"]
WORLD_H = props["height"]
WORLD_SPRITE_SIZE = props["spriteSize"]
WORLD_POKEMON_COUNT = (props["width"] * props["height"]
                       ) // 100000 if props["autoCount"] else 15


class World:
    def __init__(self, gen=True):
        self.w = WORLD_W
        self.h = WORLD_H
        self.sprite_size = WORLD_SPRITE_SIZE
        self.max_pokemon = WORLD_POKEMON_COUNT
        self.pokemon = pygame.sprite.Group()
        self.rect = pygame.Rect(0, 0, WORLD_W, WORLD_H)
        if (gen):
            self.generate_pokemon()

    def generate_pokemon(self):
        for _ in range(self.max_pokemon):
            poketype = choice([FirePokemon, GrassPokemon,
                              WaterPokemon, ElectricPokemon])
            name = choice(["Beacross", "Elesaur", "Salamoth", "Penguzz", "Steelzelle", "Slowmeleon", "Ironopotamus", "Bellosaur", "Potatoad",
                          "Scorpike", "Chimpaly", "Barrapod", "Dracung", "Hyenaring", "Hypepion", "Horromite", "Hyparos", "Magicacle", "Flyte", "Manateeth"])
            self.pokemon.add(poketype(name, randint(5, 20), randint(5, 20), randint(
                0, WORLD_W - WORLD_SPRITE_SIZE), randint(WORLD_SPRITE_SIZE, WORLD_H - WORLD_SPRITE_SIZE)))

    def draw(self, surface):
        surface.set_clip(self.rect)
        self.pokemon.draw(surface)

    def update(self):
        for pokemon in self.pokemon.sprites():
            if (pokemon.x <= 0):
                pokemon.vx = abs(pokemon.vx)
            if (pokemon.y <= WORLD_SPRITE_SIZE):
                pokemon.vy = abs(pokemon.vy)
            if (pokemon.x >= WORLD_W - WORLD_SPRITE_SIZE):
                pokemon.vx = -abs(pokemon.vx)
            if (pokemon.y >= WORLD_H - WORLD_SPRITE_SIZE):
                pokemon.vy = -abs(pokemon.vy)
            pokemon.update()
