from pokemon import *
from poketypes import *
from trainer import *
from world import *
from properties import *

import pygame
import asyncio
import threading
from websockets.server import serve


# Создаем игру и окно
FPS = props["fps"]
WIDTH = props["width"]
HEIGHT = props["height"]
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon")
clock = pygame.time.Clock()

trainer = SmartTrainer(0, 0)
opponent = SmartTrainer(WIDTH - 200, 0)
trainers = pygame.sprite.Group(trainer, opponent)
world = World()

state = 0


async def server_handler(websocket):
    async for message in websocket:
        print(message)


async def server_main():
    async with serve(server_handler, props["host"], props["port"]):
        await asyncio.Future()


def main():
    running = True
    thread = threading.Thread(target=asyncio.run, args=(server_main(),), daemon=True)
    thread.start()
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in world.pokemon.sprites():
                    if (e.pos[0] >= i.x and e.pos[0] <= i.x + props["spriteSize"] and e.pos[1] >= i.y and e.pos[1] <= i.y + props["spriteSize"]):
                        trainer.add(i)
                        i.kill()
                        break

        # Рендеринг
        screen.fill((0, 0, 0))
        world.draw(screen)
        trainers.draw(screen)
        # Обновление
        trainers.update()
        world.update()
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        clock.tick(FPS)


main()

pygame.quit()
