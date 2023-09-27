from pokemon import *
from poketypes import *
from trainer import *
from world import *
from properties import *

import pygame
import threading
import socket
import json
from time import sleep


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
world = World(False)

state = 0
side = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((props["host"], props["port"]))


def array_to_poke(x):
    out = []
    for i in x:
        type = Pokemon
        if(i[8] == "FirePokemon"): type = FirePokemon
        if(i[8] == "WaterPokemon"): type = WaterPokemon
        if(i[8] == "ElectricPokemon"): type = ElectricPokemon
        if(i[8] == "GrassPokemon"): type = GrassPokemon
        poke = type(i[8])(i[4], i[5], i[6], i[0], i[1])
        poke.vx = i[2]
        poke.vy = i[3]
        poke.hp = i[7]
        poke.id = i[9]
        out += [poke]
    return out


def update_loop():
    while True:
        request({"a": "u"})
        sleep(0.2)


def request(data):
    data = json.dumps(data, separators=(",", ":"))
    print("C->S", data)
    sock.sendall(data.encode("utf-8"))
    resp = sock.recv(1024)
    resp = resp.decode("utf-8")
    print("S->C", resp)
    return handle_res(json.loads(resp))


def handle_res(data):
    global state, side
    if (data["a"] == "q"):
        for i in array_to_poke(data["d"]):
            world.pokemon.add(i)
    elif (data["a"] == "u"):
        state = data["d"][0]
        side = 1 - data["d"][1]
        trainer.wins = data["d"][3][0]
        trainer.box = array_to_poke(data["d"][4][1])
        opponent.wins = data["d"][3][0]
        opponent.box = array_to_poke(data["d"][3][1])
        for event in data["d"][5]:
            event_data = event[1:]
            if (event[0] == "remove"):
                for i in world.pokemon.sprites():
                    if (i.id == event_data[0]):
                        i.kill()


def main():
    global state
    request({"a": "q"})
    threading.Thread(target=update_loop, daemon=True).start()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i in world.pokemon.sprites():
                    if (e.pos[0] >= i.x and e.pos[0] <= i.x + props["spriteSize"] and e.pos[1] >= i.y and e.pos[1] <= i.y + props["spriteSize"]):
                        trainer.add(i)
                        i.kill()
                        request({"a": "r", "id": i.id})
                        break

        # Рендеринг
        screen.fill((0, 0, 0))
        trainers.draw(screen)
        if(state == 0):
            world.draw(screen)
        else:
            pass
        # Обновление
        trainers.update()
        if(state == 0):
            world.update()
        else:
            pass
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        clock.tick(FPS)


main()

pygame.quit()
