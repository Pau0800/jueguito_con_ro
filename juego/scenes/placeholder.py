"""Destino temporal hasta implementar la primera cinemática."""

import pygame

from juego.scenes.base_scene import BaseScene


class Escena2Pendiente(BaseScene):
    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN and evento.key in (
            pygame.K_RETURN,
            pygame.K_SPACE,
            pygame.K_ESCAPE,
            pygame.K_e,
        ):
            from juego.scenes.menu import MenuInicio

            self.gestor.change_scene(MenuInicio)

    def update(self, _delta: float) -> None:
        del _delta

    def draw(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((10, 12, 12))
        titulo = self.gestor.fuente_grande.render(
            self.textos["ui"]["scene_two_pending"], True, (200, 191, 171)
        )
        ayuda = self.gestor.fuente.render(
            self.textos["ui"]["return_to_menu"], True, (135, 139, 130)
        )
        pantalla.blit(titulo, titulo.get_rect(center=(480, 246)))
        pantalla.blit(ayuda, ayuda.get_rect(center=(480, 307)))


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