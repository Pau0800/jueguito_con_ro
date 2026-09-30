"""Carga centralizada y cacheada de imágenes y atlas pixel art."""

from pathlib import Path

import pygame

from juego.config import RESOLUCION_INTERNA


RAIZ_ASSETS = Path(__file__).resolve().parents[2] / "assets"


class AssetLoader:
    """Mantiene una copia cacheada por ruta para evitar leer archivos por frame."""

    def __init__(self, raiz: Path = RAIZ_ASSETS) -> None:
        self.raiz = raiz
        self.imagenes: dict[tuple[str, bool], pygame.Surface] = {}
        self.atlas: dict[tuple[str, tuple[int, int]], list[list[pygame.Surface]]] = {}

    def imagen(self, ruta: str, alpha: bool = True) -> pygame.Surface | None:
        clave = (ruta, alpha)
        if clave in self.imagenes:
            return self.imagenes[clave]
        archivo = self.raiz / ruta
        if not archivo.is_file():
            return None
        try:
            imagen = pygame.image.load(str(archivo))
            if pygame.display.get_surface() is not None:
                imagen = imagen.convert_alpha() if alpha else imagen.convert()
        except pygame.error as error:
            print(f"No se pudo cargar asset '{ruta}': {error}")
            return None
        self.imagenes[clave] = imagen
        return imagen

    def atlas_personaje(
        self,
        ruta: str,
        tamano_celda: tuple[int, int],
    ) -> list[list[pygame.Surface]] | None:
        clave = (ruta, tamano_celda)
        if clave in self.atlas:
            return self.atlas[clave]
        imagen = self.imagen(ruta)
        if imagen is None:
            return None
        ancho_celda, alto_celda = tamano_celda
        if ancho_celda <= 0 or alto_celda <= 0:
            raise ValueError("El tamaño de celda del atlas debe ser positivo.")
        columnas = imagen.get_width() // ancho_celda
        filas = imagen.get_height() // alto_celda
        if columnas == 0 or filas == 0:
            raise ValueError(f"Atlas '{ruta}' más pequeño que una celda {tamano_celda}.")
        frames = [
            [
                imagen.subsurface((columna * ancho_celda, fila * alto_celda, ancho_celda, alto_celda)).copy()
                for columna in range(columnas)
            ]
            for fila in range(filas)
        ]
        self.atlas[clave] = frames
        return frames

    @staticmethod
    def escalar_pixel_perfecto(
        imagen: pygame.Surface,
        tamano: tuple[int, int] | None = None,
        escala: int = 1,
    ) -> pygame.Surface:
        if tamano is None:
            tamano = (imagen.get_width() * escala, imagen.get_height() * escala)
        return pygame.transform.scale(imagen, tamano)

    @staticmethod
    def crear_lienzo_interno() -> pygame.Surface:
        return pygame.Surface(RESOLUCION_INTERNA, pygame.SRCALPHA)


CARGADOR_ASSETS = AssetLoader()
