"""Administra escenas y fundidos de transición."""

import pygame

from juego.textos import cargar_textos
from juego.systems.fonts import cargar_fuente


class SceneManager:
    def __init__(self, pantalla: pygame.Surface) -> None:
        self.pantalla = pantalla
        self.textos = cargar_textos()
        self.fuente = cargar_fuente(28)
        self.fuente_grande = cargar_fuente(48)
        self.escena = None
        self.escena_pendiente = None
        self.estado_fundido = "quieto"
        self.opacidad = 0

    def start(self, tipo_escena: type) -> None:
        self.escena = tipo_escena(self)

    def change_scene(self, tipo_escena: type) -> None:
        if self.estado_fundido == "quieto":
            self.escena_pendiente = tipo_escena
            self.estado_fundido = "salida"

    def handle_event(self, evento: pygame.event.Event) -> None:
        if self.estado_fundido == "quieto" and self.escena is not None:
            self.escena.handle_event(evento)

    def update(self, delta: float) -> None:
        if self.estado_fundido == "quieto" and self.escena is not None:
            self.escena.update(delta)
        elif self.estado_fundido == "salida":
            self.opacidad = min(255, self.opacidad + round(640 * delta))
            if self.opacidad >= 255:
                self.escena = self.escena_pendiente(self)
                self.escena_pendiente = None
                self.estado_fundido = "entrada"
        elif self.estado_fundido == "entrada":
            self.opacidad = max(0, self.opacidad - round(640 * delta))
            if self.opacidad == 0:
                self.estado_fundido = "quieto"

    def draw(self) -> None:
        if self.escena is not None:
            self.escena.draw(self.pantalla)
        if self.opacidad:
            capa = pygame.Surface(self.pantalla.get_size())
            capa.fill((0, 0, 0))
            capa.set_alpha(self.opacidad)
            self.pantalla.blit(capa, (0, 0))