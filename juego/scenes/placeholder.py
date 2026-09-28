"""Destino temporal hasta implementar la primera cinemática."""

import pygame

from juego.scenes.base_scene import BaseScene


class CinematicaPendiente(BaseScene):
    def handle_event(self, _evento: pygame.event.Event) -> None:
        del _evento
        return

    def update(self, _delta: float) -> None:
        del _delta
        return

    def draw(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((10, 11, 13))
        titulo = self.gestor.fuente_grande.render(
            self.textos["ui"]["cinematic_placeholder"], True, (196, 190, 174)
        )
        nota = self.gestor.fuente.render(
            self.textos["ui"]["placeholder_note"], True, (121, 124, 121)
        )
        pantalla.blit(titulo, titulo.get_rect(center=(480, 245)))
        pantalla.blit(nota, nota.get_rect(center=(480, 300)))