from random import randint
import pygame

__all__ = ["Pokemon"]

current_id = 0

class Pokemon(pygame.sprite.Sprite):
    def __init__(self, name, atk, df, x, y):
        global current_id
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f"assets/{type(self).__name__}.png").convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        #self.rect.width = 400
        #pygame.transform.scale(self.image, (400, 200))
        self.name = name
        self.atk = atk
        self.df = df
        self.hp = 100
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.id = current_id
        current_id += 1
        while (self.vx == 0):
            self.vx = randint(-5, 5)
        while (self.vy == 0):
            self.vy = randint(-5, 5)

    def __str__(self):
        return f"Pokemon \"{self.name}\" ({self.hp}, {self.atk}, {self.df})"

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk

    def get_def(self):
        return self.df

    def attack(self, target, self_copy=None, target_copy=None):
        if (self_copy == None):
            self_copy = self
        if (target_copy == None):
            target_copy = target
        if (self.hp == 0):
            return
        target.hp = max(
            0, target.hp - max(self_copy.get_atk() - target_copy.get_def(), 0))

    def draw(self, surface):
        pass

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.x, self.rect.y = self.x, self.y

        surface = self.image
        surface.blit(pygame.image.load(
            f"assets/{type(self).__name__}.png").convert(), (0, 0))

        font = pygame.font.Font("haxrcorp-4089.ttf", 32)

        n = 0
        for i in [self.name, f"A{self.atk} D{self.df}"]:
            text_surface = font.render(i, True, pygame.Color(255, 0, 0))
            surface.blit(text_surface, (205, n * 40))
            n += 1
