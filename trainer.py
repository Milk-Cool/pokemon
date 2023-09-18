from poketypes import *


class Trainer:
    def __init__(self, x=0, y=0):
        self.wins = 0
        self.box = []
        self.x = x
        self.y = y
        self.screen = None

    def add(self, pokemon):
        self.box += [pokemon]

    def best_team(self, n):
        # TODO: find a better algorithm
        team = self.box[:n]
        self.box = self.box[n:]
        return team

    def draw(self, screen):
        self.screen = screen

    def update(self):
        assert (self.screen)
        