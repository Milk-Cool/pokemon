from pokemon import *
from copy import copy


class WaterPokemon(Pokemon):
    def attack(self, target):
        self_copy = copy(self)
        target_copy = copy(target)
        if (type(target) == FirePokemon):
            self_copy.atk *= 3
        super().attack(target, self_copy, target_copy)


class FirePokemon(Pokemon):
    pass


class GrassPokemon(Pokemon):
    def attack(self, target):
        self_copy = copy(self)
        target_copy = copy(target)
        if (type(target) == FirePokemon):
            target_copy.df //= 2
        super().attack(target, self_copy, target_copy)


class ElectricPokemon(Pokemon):
    def attack(self, target):
        self_copy = copy(self)
        target_copy = copy(target)
        if (type(target) == WaterPokemon):
            target_copy.df = 0
        super().attack(target, self_copy, target_copy)
