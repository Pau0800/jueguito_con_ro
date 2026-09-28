"""Punto de entrada del prototipo narrativo."""

import pygame

from juego.scenes.menu import MenuInicio
from juego.scene_manager import SceneManager


ANCHO, ALTO = 960, 540


def main() -> None:
    pygame.init()
    pygame.joystick.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Hospital psiquiátrico | Prototipo")

    gestor = SceneManager(pantalla)
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