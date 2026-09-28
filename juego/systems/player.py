"""Personaje individual con movimiento y colisión propios."""

import pygame

from juego.config import VELOCIDAD_JUGADOR
from juego.systems.collision import mover_con_colisiones
from juego.systems.input import leer_movimiento
from juego.systems.sprites import cargar_sprites_periodista


class Periodista:
    ANCHO_COLLIDER = 32
    ALTO_COLLIDER = 48

    def __init__(self, indice: int, posicion: tuple[int, int], esquema_controles: str) -> None:
        self.indice = indice
        self.esquema_controles = esquema_controles
        self.rect = pygame.Rect(
            posicion[0], posicion[1], self.ANCHO_COLLIDER, self.ALTO_COLLIDER
        )
        self.sprites = cargar_sprites_periodista(indice)
        self.direccion = "abajo"
        self.frame = 0
        self.tiempo_animacion = 0.0
        self.moviendo = False

    def update(self, delta: float, obstaculos: list[pygame.Rect]) -> None:
        direccion_x, direccion_y = leer_movimiento(self.esquema_controles)
        self.moviendo = abs(direccion_x) + abs(direccion_y) > 0.05
        if self.moviendo:
            if abs(direccion_x) > abs(direccion_y):
                self.direccion = "derecha" if direccion_x > 0 else "izquierda"
            else:
                self.direccion = "abajo" if direccion_y > 0 else "arriba"
            self.tiempo_animacion += delta
            if self.tiempo_animacion >= 0.12:
                self.frame = (self.frame % 3) + 1
                self.tiempo_animacion = 0.0
        else:
            self.frame = 0
            self.tiempo_animacion = 0.0
        mover_con_colisiones(
            self.rect,
            direccion_x * VELOCIDAD_JUGADOR * delta,
            direccion_y * VELOCIDAD_JUGADOR * delta,
            obstaculos,
        )

    def dibujar(self, pantalla: pygame.Surface) -> None:
        fotograma = self.sprites[self.direccion][self.frame]
        escalado = pygame.transform.scale(
            fotograma, (self.ANCHO_COLLIDER, self.ALTO_COLLIDER)
        )
        pantalla.blit(escalado, self.rect.topleft)