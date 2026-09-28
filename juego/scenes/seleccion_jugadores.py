"""Elección de uno o dos periodistas antes de iniciar la historia."""

import pygame

from juego import estado_juego
from juego.scenes.base_scene import BaseScene
from juego.scenes.escena_hospital import EscenaHospital
from juego.systems.fonts import cargar_fuente


class SeleccionJugadores(BaseScene):
    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        self.opcion = 0
        self.botones = [pygame.Rect(250, 300, 210, 70), pygame.Rect(500, 300, 210, 70)]
        self.fuente_titulo = cargar_fuente(52)
        self.fuente_opcion = cargar_fuente(36)

    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.MOUSEMOTION:
            for indice, boton in enumerate(self.botones):
                if boton.collidepoint(evento.pos):
                    self.opcion = indice
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for indice, boton in enumerate(self.botones):
                if boton.collidepoint(evento.pos):
                    self._iniciar(indice + 1)
        elif evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.opcion = 0
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.opcion = 1
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._iniciar(self.opcion + 1)
            elif evento.key == pygame.K_ESCAPE:
                from juego.scenes.menu import MenuInicio

                self.gestor.change_scene(MenuInicio)

    def _iniciar(self, cantidad: int) -> None:
        estado_juego.definir_cantidad_jugadores(cantidad)
        self.gestor.change_scene(EscenaHospital)

    def update(self, _delta: float) -> None:
        del _delta
        return

    def draw(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((17, 20, 20))
        pygame.draw.rect(pantalla, (34, 40, 37), (0, 0, 960, 200))
        titulo = self.fuente_titulo.render("¿CUÁNTOS PERIODISTAS?", True, (207, 197, 172))
        pantalla.blit(titulo, titulo.get_rect(center=(480, 210)))
        for indice, (boton, etiqueta) in enumerate(zip(self.botones, ("1 Jugador", "2 Jugadores"))):
            activo = indice == self.opcion
            pygame.draw.rect(pantalla, (77, 70, 57) if activo else (37, 42, 40), boton)
            pygame.draw.rect(pantalla, (144, 128, 94), boton, 2)
            texto = self.fuente_opcion.render(etiqueta, True, (224, 215, 190))
            pantalla.blit(texto, texto.get_rect(center=boton.center))
        ayuda = self.gestor.fuente.render("Flechas + Enter  |  Ratón", True, (142, 145, 135))
        pantalla.blit(ayuda, ayuda.get_rect(center=(480, 410)))