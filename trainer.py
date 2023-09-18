import pygame
from poketypes import *

__all__ = ["Trainer", "SmartTrainer"]


class Trainer(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/trainer.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.wins = 0
        self.box = []

    def add(self, pokemon):
        self.box += [pokemon]

    def best_team(self, n):
        team = self.box[:n]
        self.box = self.box[n:]
        return team

    def draw(self, surface):
        pass

    def update(self):
        surface = self.image
        surface.blit(pygame.image.load("assets/trainer.png").convert(), (0, 0))

        font = pygame.font.Font("haxrcorp-4089.ttf", 16)

        n = 0
        for i in ["Wins: " + str(self.wins), "Pokemon: " + str(len(self.box)), *map(lambda x: f"{x.name} A{x.atk} D{x.df}", self.box)]:
            text_surface = font.render(i, True, pygame.Color(255, 0, 0))
            surface.blit(text_surface, (100, n * 20 + 5))
            n += 1


class SmartTrainer(Trainer):
    def best_team(self, n):
        box = sorted(self.box, key=lambda x: (x.atk * 1.5 + x.df)
                     * (0.75 if type(x) == FirePokemon else 1), reverse=True)
        team = box[:n]
        self.box = box[n:]
        return team
