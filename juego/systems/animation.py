"""Animación reutilizable de filas de atlas con velocidad configurable."""

import pygame

from juego.config import FPS_ANIMACION_PERSONAJE, PALETA_TERROR, TAMANO_CELDA_PERSONAJE
from juego.systems.assets import CARGADOR_ASSETS


class SpriteAnimado:
    """Reproduce filas de atlas en idle, cuatro direcciones o una pose."""

    def __init__(
        self,
        indice_personaje: int,
        ruta_atlas: str | None = None,
        tamano_celda: tuple[int, int] = TAMANO_CELDA_PERSONAJE,
        fps: float = FPS_ANIMACION_PERSONAJE,
        nombres_filas: tuple[str, ...] = (
            "idle",
            "walk_down",
            "walk_left",
            "walk_right",
            "walk_up",
            "sentada",
        ),
    ) -> None:
        self.fps = fps
        self.nombres_filas = nombres_filas
        self.estado = "idle"
        self.tiempo = 0.0
        self.indice_frame = 0
        self.frames = self._cargar_o_crear(indice_personaje, ruta_atlas, tamano_celda)

    def _cargar_o_crear(
        self,
        indice: int,
        ruta: str | None,
        tamano_celda: tuple[int, int],
    ) -> dict[str, list[pygame.Surface]]:
        atlas = CARGADOR_ASSETS.atlas_personaje(ruta, tamano_celda) if ruta else None
        if atlas is not None and len(atlas) >= len(self.nombres_filas):
            return {
                nombre: atlas[indice_fila]
                for indice_fila, nombre in enumerate(self.nombres_filas)
            }
        return self._crear_frames_placeholder(indice, tamano_celda)

    def _crear_frames_placeholder(
        self, indice: int, tamano_celda: tuple[int, int]
    ) -> dict[str, list[pygame.Surface]]:
        estados = {
            "walk_down": "abajo",
            "walk_left": "izquierda",
            "walk_right": "derecha",
            "walk_up": "arriba",
        }
        filas: dict[str, list[pygame.Surface]] = {
            "idle": self._crear_placeholder_idle(indice, tamano_celda),
            "sentada": self._crear_placeholder_sentada(indice, tamano_celda),
        }
        for estado, orientacion in estados.items():
            if estado == "sentada":
                filas[estado] = self._crear_placeholder_sentada(indice, tamano_celda)
            else:
                filas[estado] = [
                    self._crear_placeholder_caminando(orientacion, frame, indice, tamano_celda)
                    for frame in range(4)
                ]
        return filas

    @staticmethod
    def _crear_placeholder_idle(
        indice: int, tamano: tuple[int, int]
    ) -> list[pygame.Surface]:
        ancho, alto = tamano
        frames: list[pygame.Surface] = []
        for respiracion in (0, 1, 0, -1):
            frame = SpriteAnimado._crear_placeholder_caminando(
                "abajo", 1, indice, tamano
            )
            escala_x, escala_y = ancho / 32, alto / 48
            pygame.draw.rect(
                frame,
                PALETA_TERROR["tela"],
                (
                    round(14 * escala_x),
                    round((26 + respiracion) * escala_y),
                    max(1, round(4 * escala_x)),
                    max(1, round(2 * escala_y)),
                ),
            )
            frames.append(frame)
        return frames

    @staticmethod
    def _crear_placeholder_caminando(
        orientacion: str,
        fotograma: int,
        indice: int,
        tamano: tuple[int, int],
    ) -> pygame.Surface:
        ancho, alto = tamano
        escala_x, escala_y = ancho / 32, alto / 48
        sprite = pygame.Surface(tamano, pygame.SRCALPHA)
        colores = PALETA_TERROR
        abrigo = (76, 91, 77) if indice in (0, 2) else (93, 72, 61)
        abrigo_luz = (113, 124, 96) if indice in (0, 2) else (132, 98, 77)
        piel = colores["piel"]
        pelo = (40, 34, 31) if indice % 2 == 0 else (61, 40, 34)
        desplazamiento = (0, 2, 0, -2)[fotograma]

        def pixel(color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
            pygame.draw.rect(
                sprite,
                color,
                (round(rect[0] * escala_x), round(rect[1] * escala_y),
                 max(1, round(rect[2] * escala_x)), max(1, round(rect[3] * escala_y))),
            )

        if orientacion == "arriba":
            pixel(colores["sombra"], (8, 5, 16, 9))
            pixel(pelo, (9, 4, 14, 9))
            pixel((69, 55, 43), (12, 6, 8, 5))
        elif orientacion in ("izquierda", "derecha"):
            pixel(colores["sombra"], (7, 5, 18, 10))
            pixel(pelo, (8, 4, 16, 10))
            pixel(piel, (9, 8, 13, 11))
            ojo_x = 12 if orientacion == "izquierda" else 20
            pixel((28, 29, 27), (ojo_x, 13, 2, 2))
            pixel((91, 66, 52), (ojo_x - 2, 16, 4, 2))
        else:
            pixel(colores["sombra"], (7, 4, 18, 11))
            pixel(pelo, (8, 3, 16, 9))
            pixel((61, 46, 36), (9, 5, 14, 4))
            pixel(piel, (10, 9, 12, 9))
            pixel((28, 29, 27), (12, 13, 2, 2))
            pixel((28, 29, 27), (19, 13, 2, 2))
            pixel((117, 69, 56), (15, 17, 3, 1))

        # Cuello, abrigo, solapas, costuras y credencial.
        pixel((28, 32, 29), (9, 19, 14, 22))
        pixel(abrigo, (7, 19, 18, 20))
        pixel(abrigo_luz, (9, 21, 5, 14))
        pixel((52, 61, 51), (18, 21, 5, 14))
        pixel((176, 161, 124), (14, 20, 4, 5))
        pixel((64, 48, 38), (15, 24, 2, 12))
        pixel((151, 134, 98), (21, 27, 3, 5))
        pixel((43, 47, 40), (21, 28, 1, 2))
        pixel((43, 47, 40), (8, 38, 16, 3))

        paso_izq, paso_der = ((-2, 2), (0, 0), (2, -2), (0, 0))[fotograma]
        pixel((48, 46, 40), (10 + paso_izq, 39, 5, 6))
        pixel((48, 46, 40), (18 + paso_der, 39, 5, 6))
        pixel((25, 26, 24), (8 + paso_izq, 44, 8, 3))
        pixel((25, 26, 24), (17 + paso_der, 44, 8, 3))

        # Brazos, manos y pliegues laterales del abrigo.
        brazo_y = 23 + desplazamiento
        pixel((53, 61, 51), (4, brazo_y, 4, 14))
        pixel((53, 61, 51), (24, brazo_y, 4, 14))
        pixel(piel, (4, brazo_y + 12, 4, 4))
        pixel(piel, (24, brazo_y + 12, 4, 4))
        pixel((132, 119, 88), (8, 34, 2, 3))
        pixel((132, 119, 88), (22, 34, 2, 3))
        return sprite

    @staticmethod
    def _crear_placeholder_sentada(
        indice: int, tamano_celda: tuple[int, int]
    ) -> list[pygame.Surface]:
        ancho, alto = tamano_celda
        ropa = (111, 107, 84) if indice < 2 else (76, 85, 75)
        piel = (168, 136, 111)
        tejido = (157, 151, 128)
        frames: list[pygame.Surface] = []
        for respiracion in (0, 1, 0, -1):
            frame = pygame.Surface(tamano_celda, pygame.SRCALPHA)
            escala_x, escala_y = ancho / 32, alto / 48
            def bloque(color: tuple[int, int, int], rect: tuple[int, int, int, int]) -> None:
                pygame.draw.rect(
                    frame,
                    color,
                    (round(rect[0] * escala_x), round(rect[1] * escala_y),
                     max(1, round(rect[2] * escala_x)), max(1, round(rect[3] * escala_y))),
                )
            bloque((49, 38, 33), (8, 4 + respiracion, 16, 13))
            bloque(piel, (10, 8 + respiracion, 12, 12))
            bloque((31, 31, 29), (12, 13 + respiracion, 2, 2))
            bloque((31, 31, 29), (19, 13 + respiracion, 2, 2))
            bloque(ropa, (8, 20 + respiracion, 16, 14))
            bloque(tejido, (5, 24 + respiracion, 22, 4))
            bloque((92, 88, 72), (8, 29 + respiracion, 16, 3))
            bloque(tejido, (11, 21 + respiracion, 10, 3))
            bloque((63, 59, 49), (14, 21 + respiracion, 4, 13))
            bloque((81, 73, 58), (4, 34, 24, 8))
            bloque((53, 48, 41), (3, 41, 26, 3))
            frames.append(frame)
        return frames

    def seleccionar(self, estado: str) -> None:
        if estado not in self.frames:
            raise KeyError(f"No existe la animación '{estado}'.")
        if self.estado != estado:
            self.estado = estado
            self.indice_frame = 0
            self.tiempo = 0.0

    def update(self, delta: float) -> None:
        frames = self.frames[self.estado]
        if len(frames) <= 1:
            return
        self.tiempo += delta
        intervalo = 1.0 / max(self.fps, 0.01)
        while self.tiempo >= intervalo:
            self.tiempo -= intervalo
            self.indice_frame = (self.indice_frame + 1) % len(frames)

    @property
    def imagen_actual(self) -> pygame.Surface:
        return self.frames[self.estado][self.indice_frame]

    def dibujar(
        self,
        destino: pygame.Surface,
        posicion: tuple[int, int],
        tamano: tuple[int, int] | None = None,
    escala: int = 1,
    ) -> None:
        imagen = self.imagen_actual
        if tamano is None:
            tamano = (imagen.get_width() * escala, imagen.get_height() * escala)
        dibujada = pygame.transform.scale(imagen, tamano)
        destino.blit(dibujada, posicion)
