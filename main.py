#!python3.13
"""Punto de entrada del prototipo narrativo."""

import sys

import pygame

from juego.scenes.menu import MenuInicio
from juego.scenes.cinematica_2 import Cinematica2
from juego.scene_manager import SceneManager


ANCHO, ALTO = 960, 540


def main() -> None:
    pygame.init()
    pygame.joystick.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Hospital psiquiátrico | Prototipo")

    gestor = SceneManager(pantalla)
    if "--cinematica2" in sys.argv:
        print("[DEBUG] Argumento --cinematica2 detectado: iniciando directamente en Cinemática 2.")
        gestor.start(Cinematica2)
    else:
        gestor.start(MenuInicio)
    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        delta = min(reloj.tick(60) / 1000.0, 0.05)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            else:
                gestor.handle_event(evento)

        gestor.update(delta)
        gestor.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()