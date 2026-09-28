"""Movimiento por ejes con colisión rectangular."""

import pygame
import math


def mover_con_colisiones(
    rectangulo: pygame.Rect,
    desplazamiento_x: float,
    desplazamiento_y: float,
    obstaculos: list[pygame.Rect],
) -> None:
    """Mueve el rectángulo y lo separa de los obstáculos sólidos."""
    pasos = max(1, math.ceil(max(abs(desplazamiento_x), abs(desplazamiento_y)) / 4))
    paso_x = desplazamiento_x / pasos
    paso_y = desplazamiento_y / pasos

    for _ in range(pasos):
        rectangulo.x += round(paso_x)
        for obstaculo in obstaculos:
            if rectangulo.colliderect(obstaculo):
                if paso_x > 0:
                    rectangulo.right = obstaculo.left
                elif paso_x < 0:
                    rectangulo.left = obstaculo.right

        rectangulo.y += round(paso_y)
        for obstaculo in obstaculos:
            if rectangulo.colliderect(obstaculo):
                if paso_y > 0:
                    rectangulo.bottom = obstaculo.top
                elif paso_y < 0:
                    rectangulo.top = obstaculo.bottom