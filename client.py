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


packet_lock = False

# Создаем игру и окно
FPS = props["fps"]
WIDTH = props["width"]
HEIGHT = props["height"]
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Pokémon")
clock = pygame.time.Clock()

trainer = SmartTrainer(0, 0)
opponent = SmartTrainer(WIDTH - props["spriteSize"], 0)
trainer_pokemon_battle = pygame.sprite.Group()
opponent_pokemon_battle = pygame.sprite.Group()
trainers = pygame.sprite.Group(trainer, opponent)
world = World(False)

battle_state = 0
state = 0
last_state = 0
side = 0
sel = -1
sel_opponent = -1

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((props["host"], props["port"]))


def array_to_poke(x):
    out = []
    for i in x:
        type = Pokemon
        if (i[8] == "FirePokemon"):
            type = FirePokemon
        if (i[8] == "WaterPokemon"):
            type = WaterPokemon
        if (i[8] == "ElectricPokemon"):
            type = ElectricPokemon
        if (i[8] == "GrassPokemon"):
            type = GrassPokemon
        poke = type(i[4], i[5], i[6], i[0], i[1])
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
    global packet_lock
    data = json.dumps(data, separators=(",", ":"))
    print("C->S", data)
    while (packet_lock):
        sleep(0.01)
    packet_lock = True
    sock.sendall(data.encode("utf-8"))
    resp = sock.recv(1024)
    packet_lock = False
    resp = resp.decode("utf-8")
    print("S->C", resp)
    return handle_res(json.loads(resp))


def handle_res(data):
    global state, side, battle_state
    if (data["a"] == "q"):
        for i in array_to_poke(data["d"]):
            world.pokemon.add(i)
    elif (data["a"] == "u"):
        state = data["d"][0]
        side = 1 - data["d"][1]
        trainer.wins = data["d"][4][0]
        trainer.box = array_to_poke(data["d"][4][1])
        opponent.wins = data["d"][3][0]
        opponent.box = array_to_poke(data["d"][3][1])
        for event in data["d"][5]:
            event_data = event[1:]
            if (event[0] == "remove"):
                for i in world.pokemon.sprites():
                    if (i.id == event_data[0]):
                        i.kill()
            elif (event[0] == "update_hp"):
                flag = True
                for i in trainer_pokemon_battle.sprites():
                    if (i.id == event_data[0]):
                        i.hp = event_data[1]
                        if (i.hp == 0):
                            i.kill()
                        flag = False
                if (flag):
                    for i in opponent_pokemon_battle.sprites():
                        if (i.id == event_data[0]):
                            i.hp = event_data[1]
                            if (i.hp == 0):
                                i.kill()
                            flag = False
    elif (data["a"] == "f"):
        trainer_pokemon_battle.empty()
        trainer_pokemon_battle.add(*array_to_poke(data["d"][1]))
        opponent_pokemon_battle.empty()
        opponent_pokemon_battle.add(*array_to_poke(data["d"][0]))


def main():
    global events, state, side, battle_state, sel, sel_opponent, last_state
    request({"a": "q"})
    threading.Thread(target=update_loop, daemon=True).start()
    running = True
    while running:
        if (last_state != state):
            if (state == 0):
                request({"a": "q"})
            elif (state == 1):
                request({"a": "f"})
            last_state = state

        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and state == 0:
                for i in world.pokemon.sprites():
                    if (e.pos[0] >= i.x and e.pos[0] <= i.x + props["spriteSize"] and e.pos[1] >= i.y and e.pos[1] <= i.y + props["spriteSize"]):
                        trainer.add(i)
                        i.kill()
                        request({"a": "r", "id": i.id})
                        break
            if e.type == pygame.MOUSEBUTTONDOWN and state == 1 and side == 0:
                if (battle_state == 0):
                    for i in trainer_pokemon_battle.sprites():
                        if (e.pos[0] >= i.x and e.pos[0] <= i.x + props["spriteSize"] and e.pos[1] >= i.y and e.pos[1] <= i.y + props["spriteSize"]):
                            sel = i.id
                            battle_state = 1
                            break
                if (battle_state == 1):
                    for i in opponent_pokemon_battle.sprites():
                        if (e.pos[0] >= i.x and e.pos[0] <= i.x + props["spriteSize"] and e.pos[1] >= i.y and e.pos[1] <= i.y + props["spriteSize"]):
                            sel_opponent = i.id
                            request({"a": "b", "d": [sel, sel_opponent]})
                            sel = -1
                            sel_opponent = -1
                            battle_state = 0
                            break

        # Рендеринг
        sel_color = (240, 240, 240)
        screen.fill((0, 0, 0))
        trainers.draw(screen)
        if (state == 0):
            world.draw(screen)
        elif (state == 1):
            trainer_pokemon_battle.draw(screen)
            opponent_pokemon_battle.draw(screen)
        # Обновление
        trainers.update()
        if (state == 0):
            world.update()
        elif (state == 1):
            trainer_pokemon_battle.update()
            opponent_pokemon_battle.update()
            pygame.draw.rect(screen, (240, 240, 240), pygame.Rect(
                0 if side == 0 else WIDTH - props["spriteSize"], props["spriteSize"], props["spriteSize"], 5))
            if (sel != -1):
                sel_y = list(filter(lambda x: x.id == sel,
                             trainer_pokemon_battle.sprites()))[0].y
                pygame.draw.rect(screen, sel_color, pygame.Rect(
                    0, sel_y + props["spriteSize"], props["spriteSize"], 5))
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()


main()

pygame.quit()
