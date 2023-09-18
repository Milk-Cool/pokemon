import pygame
from poketypes import *

__all__ = ["Trainer"]


# def drawText(surface, color, text, where, font_name = "Arial", font_size = 16):
#     font = pygame.font.SysFont(font_name, font_size)
#     text_surface = font.render(text, True, color)
#     text_rect = text_surface.get_rect()
#     if type(where) is pygame.Rect:
#         text_rect.center = where.center
#     else:
#         text_rect.topleft = where
#     surface.blit(text_surface, text_rect)

class Trainer(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/trainer.png").convert()
        self.rect = pygame.Rect(x, y, 200, 200)
        self.wins = 0
        self.box = []
        self.x = x
        self.y = y

    def add(self, pokemon):
        self.box += [pokemon]

    def best_team(self, n):
        # TODO: find a better algorithm
        team = self.box[:n]
        self.box = self.box[n:]
        return team

    def draw(self, surface):
        pass

    def update(self):
        surface = self.image

        font = pygame.font.SysFont("Dax Pro Regular", 16)

        n = 0
        for i in ["Wins: " + str(self.wins), "Pokemon: " + str(len(self.box)), *map(lambda x: x.name, self.box)]:
            text_surface = font.render(i, True, pygame.Color(0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.x + 100, n * 20 + 5)
            surface.blit(text_surface, text_rect)
            # drawText(surface, pygame.Color(0,0,0), i, (self.x + 100, n * 20 + 5))
            n += 1
