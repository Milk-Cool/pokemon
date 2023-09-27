from pokemon import *
from poketypes import *
from trainer import *
from world import *
from properties import *

import pygame
import threading
import socket
import json


# Создаем игру и окно
FPS = props["fps"]
WIDTH = props["width"]
HEIGHT = props["height"]
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon")
clock = pygame.time.Clock()

# Массив событий
events = []

trainer = SmartTrainer(0, 0)
trainer.wins = 5
opponent = SmartTrainer(WIDTH - 200, 0)
trainers = pygame.sprite.Group(trainer, opponent)
world = World()

state = 0
side = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((props["host"], props["port"]))
except socket.error as e:
    print(str(e))

sock.listen(2)


def start_battle():
    global state, side
    state = 1
    side = 0


def respond(conn, data):
    print("S->C", data)
    conn.sendall(data.encode("utf-8"))


def poke_to_array(poke):
    return [poke.x, poke.y, poke.vx, poke.vy, poke.name,
            poke.atk, poke.df, poke.hp, type(poke).__name__, poke.id]


def handle_req(data):
    global events, state
    resp = None
    if (data["a"] == "q"):  # Отправить данные покемонов
        resp = list(map(poke_to_array, world.pokemon.sprites()))
    elif (data["a"] == "u"):
        resp = [state, side, list(map(poke_to_array, world.pokemon.sprites())), [trainer.wins, list(map(poke_to_array, trainer.box))], [
            opponent.wins, list(map(poke_to_array, opponent.box))], events]
        events = []
    elif (data["a"] == "r"):
        resp = True
        for i in world.pokemon.sprites():
            if (i.id == data["id"]):
                i.kill()
                opponent.add(i)
                if (len(world.pokemon.sprites()) == 0):
                    start_battle()
    return json.dumps({"a": data["a"], "d": resp}, separators=(",", ":"))


def socket_handler():
    while True:
        # Сокеты
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)  # Up to 1024 bytes
                if not data:
                    break
                data_str = str(data, "utf-8")
                print("C->S", data_str)
                data_json = json.loads(data_str)
                resp = handle_req(data_json)
                respond(conn, resp)


def main():
    global events, state, side
    threading.Thread(target=socket_handler, daemon=True).start()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN and state == 0:
                for i in world.pokemon.sprites():
                    if (e.pos[0] >= i.x and e.pos[0] <= i.x + props["spriteSize"] and e.pos[1] >= i.y and e.pos[1] <= i.y + props["spriteSize"]):
                        trainer.add(i)
                        events += [["remove", i.id]]
                        i.kill()
                        if (len(world.pokemon.sprites()) == 0):
                            start_battle()
                        break

        # Рендеринг
        screen.fill((0, 0, 0))
        trainers.draw(screen)
        if (state == 0):
            world.draw(screen)
        else:
            pass
        # Обновление
        trainers.update()
        if (state == 0):
            world.update()
        else:
            pass
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()
        clock.tick(FPS)


main()

pygame.quit()
