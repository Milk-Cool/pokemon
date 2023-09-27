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

trainer = SmartTrainer(0, 0)
opponent = SmartTrainer(WIDTH - 200, 0)
trainers = pygame.sprite.Group(trainer, opponent)
world = World()

state = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((props["host"], props["port"]))
except socket.error as e:
    print(str(e))

sock.listen(2)


def respond(conn, data):
    print("S->C", data)
    conn.sendall(data.encode("utf-8"))


def handle_req(data):
    resp = None
    if (data["a"] == "q"):  # Запросить данные покемонов
        resp = list(map(lambda x: [x.x, x.y, x.vx, x.vy, x.name,
                   x.atk, x.df, x.hp], world.pokemon.sprites()))
    return json.dumps(resp)


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
    threading.Thread(target=socket_handler, daemon=True).start()
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
