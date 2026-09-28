"""Carga una fuente pixel opcional y conserva una fuente de reserva."""

from pathlib import Path
from functools import lru_cache

import pygame


@lru_cache(maxsize=16)
def cargar_fuente(tamano: int) -> pygame.font.Font:
    ruta = Path(__file__).resolve().parents[2] / "assets" / "fonts" / "pixel.ttf"
    if ruta.exists():
        try:
            return pygame.font.Font(str(ruta), tamano)
        except pygame.error:
            pass
    return pygame.font.Font(None, tamano)