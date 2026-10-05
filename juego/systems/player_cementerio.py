"""Movimiento lateral y colisiones compartidos por los serenos."""

import pygame

from juego.config import (
    ALTO_COLLIDER_CEMENTERIO,
    ALTURA_SUELO_CEMENTERIO,
    ANCHO_COLLIDER_CEMENTERIO,
    DURACION_CAIDA_TUMBA,
    DURACION_SALIDA_RESCATE,
    FUERZA_SALTO_CEMENTERIO,
    GRAVEDAD_CEMENTERIO,
    VELOCIDAD_ANIMACION_CEMENTERIO,
    VELOCIDAD_CEMENTERIO,
)
from juego.systems.animation import SpriteAnimado
from juego.systems.collision import mover_con_colisiones
from juego.systems.input import leer_movimiento


class JugadorCementerio:
    """Usa la misma física para ambos jugadores; cambia únicamente sus teclas."""

    def __init__(self, indice: int, posicion_x: float, esquema_controles: str) -> None:
        self.indice = indice
        self.esquema_controles = esquema_controles
        self.rect = pygame.Rect(
            round(posicion_x),
            ALTURA_SUELO_CEMENTERIO - ALTO_COLLIDER_CEMENTERIO,
            ANCHO_COLLIDER_CEMENTERIO,
            ALTO_COLLIDER_CEMENTERIO,
        )
        self.velocidad_vertical = 0.0
        self.en_suelo = True
        self.moviendo = False
        self.direccion = "derecha"
        self.resto_movimiento_x = 0.0
        self.estado = "normal"
        self.tiempo_caida = 0.0
        self.x_ultima_segura = float(posicion_x)
        self.posicion_pozo: float | None = None
        self.animacion = SpriteAnimado(
            indice + 4,
            f"sprites/personajes/sereno_{indice + 1}/atlas.png",
            fps=VELOCIDAD_ANIMACION_CEMENTERIO,
        )

    def saltar(self) -> bool:
        if not self.en_suelo:
            return False
        self.velocidad_vertical = -FUERZA_SALTO_CEMENTERIO
        self.en_suelo = False
        return True

    def update(
        self,
        delta: float,
        obstaculos: list[pygame.Rect],
        limite_x: tuple[float, float],
        pozos: list[tuple[int, int]],
    ) -> None:
        if self.estado in ("cayendo", "saliendo"):
            self.tiempo_caida += delta
            if self.estado == "cayendo" and self.tiempo_caida >= DURACION_CAIDA_TUMBA:
                self.estado = "caido"
            elif self.estado == "saliendo" and self.tiempo_caida >= DURACION_SALIDA_RESCATE:
                self.estado = "normal"
                self.tiempo_caida = 0.0
            return
        if self.estado != "normal":
            return

        direccion_x, _ = leer_movimiento(self.esquema_controles)
        self.resto_movimiento_x += direccion_x * VELOCIDAD_CEMENTERIO * delta
        desplazamiento_x = round(self.resto_movimiento_x)
        self.resto_movimiento_x -= desplazamiento_x
        self.moviendo = abs(direccion_x) > 0.05
        if direccion_x:
            self.direccion = "derecha" if direccion_x > 0 else "izquierda"
            self.animacion.seleccionar("walk_right")
        else:
            self.animacion.seleccionar("idle")
        self.animacion.update(delta)

        obstaculos_laterales = [
            obstaculo
            for obstaculo in obstaculos
            if not (self.en_suelo and abs(self.rect.bottom - obstaculo.top) <= 1)
        ]
        x_anterior = self.rect.x
        mover_con_colisiones(self.rect, desplazamiento_x, 0, obstaculos_laterales)
        if self.rect.x != x_anterior + desplazamiento_x:
            self.resto_movimiento_x = 0.0
        self.rect.x = round(min(max(self.rect.x, limite_x[0]), limite_x[1]))

        desplazamiento_y = self.velocidad_vertical * delta
        self.velocidad_vertical += GRAVEDAD_CEMENTERIO * delta
        borde_inferior_anterior = self.rect.bottom
        self.rect.y += round(desplazamiento_y)
        self.en_suelo = False
        if self.rect.bottom >= ALTURA_SUELO_CEMENTERIO:
            self.rect.bottom = ALTURA_SUELO_CEMENTERIO
            self.velocidad_vertical = 0.0
            self.en_suelo = True
        elif desplazamiento_y >= 0:
            for obstaculo in obstaculos:
                if self.rect.colliderect(obstaculo) and borde_inferior_anterior <= obstaculo.top:
                    self.rect.bottom = obstaculo.top
                    self.velocidad_vertical = 0.0
                    self.en_suelo = True
                    break

        sobre_suelo = self.rect.bottom >= ALTURA_SUELO_CEMENTERIO
        if self.en_suelo and sobre_suelo:
            pozo_actual = next(
                (pozo for pozo in pozos if self.rect.right > pozo[0] and self.rect.left < pozo[1]),
                None,
            )
            if pozo_actual is not None:
                self.estado = "cayendo"
                self.tiempo_caida = 0.0
                self.posicion_pozo = (pozo_actual[0] + pozo_actual[1]) / 2
            else:
                self.x_ultima_segura = float(self.rect.x)

    def dibujar(self, pantalla: pygame.Surface, camara_x: float) -> None:
        imagen = self.animacion.imagen_actual
        if self.direccion == "izquierda":
            imagen = pygame.transform.flip(imagen, True, False)
        if self.estado == "cayendo":
            desplazamiento_caida = round(min(36.0, self.tiempo_caida * 88.0))
        elif self.estado == "caido":
            desplazamiento_caida = 36
        elif self.estado == "saliendo":
            progreso = min(1.0, self.tiempo_caida / DURACION_SALIDA_RESCATE)
            desplazamiento_caida = round(36 * (1.0 - progreso))
        else:
            desplazamiento_caida = 0
        posicion = (
            round(self.rect.centerx - 16 - camara_x),
            self.rect.bottom - 48 + desplazamiento_caida,
        )
        pantalla.blit(imagen, posicion)

    def iniciar_rescate(self) -> None:
        """Prepara la salida desde el último punto seguro junto al pozo."""
        if self.estado != "caido":
            return
        self.rect.x = round(self.x_ultima_segura)
        self.rect.bottom = ALTURA_SUELO_CEMENTERIO
        self.estado = "saliendo"
        self.tiempo_caida = 0.0
