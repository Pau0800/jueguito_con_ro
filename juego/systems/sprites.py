"""Carga atlases opcionales y crea sprites pixel art temporales."""

from pathlib import Path

import pygame


ANCHO_CELDA = 16
ALTO_CELDA = 24
ORDEN_DIRECCIONES = ("abajo", "izquierda", "derecha", "arriba")


def cargar_sprites_periodista(indice: int) -> dict[str, list[pygame.Surface]]:
    nombre = f"atlas_periodista_{indice + 1}.png"
    ruta = Path(__file__).resolve().parents[2] / "assets" / "sprites" / "players" / nombre
    if ruta.exists():
        atlas = pygame.image.load(str(ruta))
        if pygame.display.get_surface() is not None:
            atlas = atlas.convert_alpha()
        return {
            direccion: [
                atlas.subsurface(
                    (frame * ANCHO_CELDA, fila * ALTO_CELDA, ANCHO_CELDA, ALTO_CELDA)
                ).copy()
                for frame in range(4)
            ]
            for fila, direccion in enumerate(ORDEN_DIRECCIONES)
        }

    return {
        direccion: [
            _crear_frame(direccion, frame, indice) for frame in range(4)
        ]
        for direccion in ORDEN_DIRECCIONES
    }


def _crear_frame(direccion: str, frame: int, indice: int) -> pygame.Surface:
    sprite = pygame.Surface((ANCHO_CELDA, ALTO_CELDA), pygame.SRCALPHA)
    abrigo = (76, 98, 88) if indice == 0 else (112, 73, 66)
    abrigo_claro = (119, 132, 105) if indice == 0 else (153, 106, 86)
    piel = (174, 142, 113) if indice == 0 else (190, 151, 119)
    pelo = (39, 35, 31) if indice == 0 else (53, 35, 31)
    pantalon = (45, 49, 45)

    if direccion == "arriba":
        _rect(sprite, pelo, (4, 2, 8, 6))
        _rect(sprite, (72, 57, 43), (5, 3, 6, 4))
        _rect(sprite, abrigo, (3, 8, 10, 9))
        _rect(sprite, abrigo_claro, (6, 8, 4, 7))
        _rect(sprite, (82, 64, 48), (7, 10, 2, 4))
        _rect(sprite, piel, (2, 9, 2, 7))
        _rect(sprite, piel, (12, 9, 2, 7))
    elif direccion in ("izquierda", "derecha"):
        espejo = direccion == "derecha"
        _rect(sprite, pelo, (4, 2, 8, 7))
        _rect(sprite, piel, (4, 5, 7, 6))
        _rect(sprite, (37, 38, 33), (5 if not espejo else 10, 7, 1, 1))
        _rect(sprite, abrigo, (3, 11, 10, 9))
        _rect(sprite, abrigo_claro, (5, 12, 5, 6))
        _rect(sprite, (71, 55, 43), (8, 13, 2, 5))
        _rect(sprite, piel, (2, 12, 2, 6))
        _rect(sprite, piel, (12, 12, 2, 6))
    else:
        _rect(sprite, pelo, (4, 1, 8, 7))
        _rect(sprite, (68, 49, 37), (5, 3, 6, 2))
        _rect(sprite, piel, (5, 7, 6, 4))
        _rect(sprite, (40, 39, 34), (6, 8, 1, 1))
        _rect(sprite, (40, 39, 34), (9, 8, 1, 1))
        _rect(sprite, abrigo, (3, 11, 10, 9))
        _rect(sprite, abrigo_claro, (5, 12, 6, 4))
        _rect(sprite, (85, 63, 47), (7, 13, 2, 5))
        _rect(sprite, piel, (1, 12, 2, 5))
        _rect(sprite, piel, (13, 12, 2, 5))

    # Variar los pies entre fotogramas produce una caminata corta y legible.
    desplazamiento = (0, 1, 0, -1)[frame]
    if frame in (1, 3):
        _rect(sprite, abrigo, (2, 13, 2, 4))
        _rect(sprite, abrigo, (12, 13, 2, 4))
    pierna_izquierda = 4 - desplazamiento
    pierna_derecha = 9 + desplazamiento
    _rect(sprite, pantalon, (pierna_izquierda, 18, 3, 4))
    _rect(sprite, pantalon, (pierna_derecha, 18, 3, 4))
    _rect(sprite, (34, 31, 29), (pierna_izquierda - 1, 22, 4, 2))
    _rect(sprite, (34, 31, 29), (pierna_derecha - 1, 22, 4, 2))
    _rect(sprite, (171, 147, 114), (3, 12, 1, 2))
    return sprite


def _rect(superficie: pygame.Surface, color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
    pygame.draw.rect(superficie, color, rect)