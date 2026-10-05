"""Destino temporal hasta implementar la primera cinemática."""

import pygame

from juego.scenes.base_scene import BaseScene


class Escena2Pendiente(BaseScene):
    """Conserva el destino de la Cinemática 1 y delega al cementerio."""

    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        from juego.scenes.escena_cementerio import EscenaCementerio

        self.escena = EscenaCementerio(gestor)

    def handle_event(self, evento: pygame.event.Event) -> None:
        self.escena.handle_event(evento)

    def update(self, delta: float) -> None:
        self.escena.update(delta)

    def draw(self, pantalla: pygame.Surface) -> None:
        self.escena.draw(pantalla)


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


class Cinematica2Pendiente(BaseScene):
    """Destino temporal al completar el cementerio."""

    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN and evento.key in (
            pygame.K_RETURN,
            pygame.K_SPACE,
            pygame.K_ESCAPE,
        ):
            from juego.scenes.menu import MenuInicio

            self.gestor.change_scene(MenuInicio)

    def update(self, _delta: float) -> None:
        del _delta

    def draw(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((8, 11, 12))
        titulo = self.gestor.fuente_grande.render(
            self.textos["ui"]["cinematic_2_pending"], True, (195, 189, 173)
        )
        pantalla.blit(titulo, titulo.get_rect(center=(480, 255)))