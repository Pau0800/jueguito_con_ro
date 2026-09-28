"""Fondos pixel art, luces y textura atmosférica para el hospital."""

import math
import random
from pathlib import Path

import pygame


ANCHO, ALTO = 960, 540


class AmbienteHospital:
    def __init__(self) -> None:
        self.fondos = {
            zona: self._cargar_o_crear_fondo(zona)
            for zona in ("recepcion", "sala1", "sala2")
        }
        self.grano = self._crear_grano()
        self.vineta = self._crear_vineta()

    def _cargar_o_crear_fondo(self, zona: str) -> pygame.Surface:
        ruta = Path(__file__).resolve().parents[2] / "assets" / "images" / "backgrounds" / f"{zona}.png"
        if ruta.exists():
            imagen = pygame.image.load(str(ruta))
            if pygame.display.get_surface() is not None:
                imagen = imagen.convert()
            return pygame.transform.scale(imagen, (ANCHO, ALTO))
        return self._crear_fondo(zona)

    def _crear_fondo(self, zona: str) -> pygame.Surface:
        superficie = pygame.Surface((ANCHO, ALTO))
        semilla = {"recepcion": 11, "sala1": 23, "sala2": 47}[zona]
        azar = random.Random(semilla)
        suelo_y = 155 if zona == "recepcion" else 92
        pared = (42, 49, 43) if zona != "sala2" else (48, 42, 38)
        suelo = (38, 43, 39) if zona != "sala2" else (44, 39, 35)
        superficie.fill(pared)
        pygame.draw.rect(superficie, suelo, (0, suelo_y, ANCHO, ALTO - suelo_y))

        # Baldosas gastadas y juntas desiguales en el piso.
        for y in range(suelo_y, ALTO, 34):
            pygame.draw.line(superficie, (54, 57, 49), (0, y), (ANCHO, y), 2)
            offset = 17 if ((y - suelo_y) // 34) % 2 else 0
            for x in range(offset, ANCHO, 66):
                pygame.draw.line(superficie, (54, 57, 49), (x, y), (x, min(y + 34, ALTO)), 2)
        for _ in range(150):
            x, y = azar.randrange(ANCHO), azar.randrange(suelo_y, ALTO)
            color = azar.choice(((48, 51, 46), (31, 36, 34), (59, 55, 45), (66, 57, 48)))
            pygame.draw.rect(superficie, color, (x, y, azar.randrange(2, 9), azar.randrange(1, 4)))

        # Zócalo y paredes con desconchones, grietas y manchas envejecidas.
        pygame.draw.rect(superficie, (24, 30, 28), (0, suelo_y - 12, ANCHO, 14))
        pygame.draw.line(superficie, (100, 91, 69), (0, suelo_y - 12), (ANCHO, suelo_y - 12), 2)
        for _ in range(68):
            x, y = azar.randrange(12, ANCHO - 12), azar.randrange(12, suelo_y - 16)
            pygame.draw.rect(superficie, azar.choice(((52, 55, 46), (35, 43, 40), (59, 49, 41))),
                             (x, y, azar.randrange(3, 14), azar.randrange(2, 8)))
        for x, y, ancho in ((92, 48, 22), (236, 119, 16), (846, 57, 24), (712, 123, 18)):
            pygame.draw.lines(superficie, (22, 28, 26), False,
                              ((x, y), (x + 5, y + 9), (x + 2, y + 19), (x + ancho, y + 32)), 2)

        self._dibujar_luz_techo(superficie, 240, 41)
        self._dibujar_luz_techo(superficie, 720, 41)
        self._dibujar_marcos(superficie, suelo_y)
        if zona == "recepcion":
            self._dibujar_recepcion(superficie)
        else:
            self._dibujar_puertas(superficie, zona)
            self._dibujar_mobiliario(superficie, zona)
        return superficie

    @staticmethod
    def _dibujar_luz_techo(superficie: pygame.Surface, x: int, y: int) -> None:
        pygame.draw.rect(superficie, (26, 31, 29), (x - 50, y - 7, 100, 20))
        pygame.draw.rect(superficie, (120, 132, 112), (x - 43, y - 3, 86, 8))
        pygame.draw.line(superficie, (196, 188, 145), (x - 33, y), (x + 28, y), 2)
        pygame.draw.rect(superficie, (31, 34, 31), (x - 53, y + 12, 6, 5))
        pygame.draw.rect(superficie, (31, 34, 31), (x + 47, y + 12, 6, 5))

    @staticmethod
    def _dibujar_marcos(superficie: pygame.Surface, suelo_y: int) -> None:
        for x, y, ancho, alto in ((95, 76, 70, 52), (805, 85, 72, 45)):
            pygame.draw.rect(superficie, (31, 32, 27), (x - 3, y - 3, ancho + 6, alto + 6))
            pygame.draw.rect(superficie, (113, 96, 65), (x, y, ancho, alto), 3)
            pygame.draw.rect(superficie, (61, 67, 55), (x + 5, y + 5, ancho - 10, alto - 10))
            pygame.draw.line(superficie, (82, 83, 66), (x + 12, y + 12), (x + ancho - 14, y + alto - 15), 2)
        pygame.draw.rect(superficie, (26, 32, 30), (20, suelo_y + 3, 920, 6))

    @staticmethod
    def _dibujar_recepcion(superficie: pygame.Surface) -> None:
        pygame.draw.rect(superficie, (33, 38, 35), (0, 150, 960, 14))
        pygame.draw.rect(superficie, (72, 65, 50), (260, 183, 440, 77))
        pygame.draw.rect(superficie, (133, 115, 79), (250, 174, 460, 17))
        pygame.draw.rect(superficie, (31, 33, 29), (263, 191, 434, 9))
        pygame.draw.rect(superficie, (55, 59, 51), (280, 202, 400, 49))
        pygame.draw.rect(superficie, (91, 79, 58), (285, 206, 390, 4))
        for x in (293, 665):
            pygame.draw.rect(superficie, (27, 31, 29), (x, 246, 11, 26))
            pygame.draw.rect(superficie, (98, 84, 60), (x - 3, 270, 18, 5))
        # Recepcionista tras el mostrador, con uniforme, cuello e identificación.
        pygame.draw.rect(superficie, (24, 26, 24), (453, 117, 55, 63))
        pygame.draw.rect(superficie, (177, 146, 116), (467, 112, 28, 28))
        pygame.draw.rect(superficie, (45, 37, 32), (463, 109, 35, 12))
        pygame.draw.rect(superficie, (72, 84, 73), (459, 138, 44, 43))
        pygame.draw.rect(superficie, (187, 173, 137), (474, 140, 12, 21))
        pygame.draw.rect(superficie, (142, 130, 102), (493, 148, 5, 8))
        pygame.draw.rect(superficie, (30, 32, 29), (470, 122, 4, 3))
        pygame.draw.rect(superficie, (30, 32, 29), (488, 122, 4, 3))
        # Teléfono, papeles, silla de espera y dispensador antiguo.
        pygame.draw.rect(superficie, (29, 33, 30), (535, 164, 28, 10))
        pygame.draw.rect(superficie, (163, 154, 123), (583, 168, 44, 5))
        pygame.draw.rect(superficie, (36, 40, 36), (72, 361, 78, 51))
        pygame.draw.rect(superficie, (78, 71, 57), (76, 354, 70, 16))
        pygame.draw.rect(superficie, (28, 33, 30), (78, 411, 7, 22))
        pygame.draw.rect(superficie, (28, 33, 30), (137, 411, 7, 22))
        pygame.draw.rect(superficie, (74, 67, 54), (836, 193, 52, 99))
        pygame.draw.rect(superficie, (135, 119, 84), (844, 204, 36, 74), 2)
        pygame.draw.rect(superficie, (30, 35, 32), (855, 215, 14, 49))
        pygame.draw.rect(superficie, (120, 57, 46), (43, 205, 115, 41))
        pygame.draw.rect(superficie, (202, 185, 149), (51, 214, 99, 4))

    @staticmethod
    def _dibujar_puertas(superficie: pygame.Surface, zona: str) -> None:
        posiciones = ((170, "arriba"), (390, "arriba"), (610, "abajo"))
        if zona == "sala1":
            posiciones += ((810, "abajo"),)
        for x, lado in posiciones:
            y = 55 if lado == "arriba" else 415
            rect = pygame.Rect(x - 40, y, 80, 82)
            pygame.draw.rect(superficie, (24, 28, 26), rect.inflate(8, 7))
            pygame.draw.rect(superficie, (113, 91, 64), rect, 4)
            pygame.draw.rect(superficie, (54, 52, 43), rect.inflate(-9, -8))
            pygame.draw.rect(superficie, (33, 36, 32), (x - 27, y + 10, 54, 63))
            pygame.draw.rect(superficie, (112, 94, 66), (x + 20, y + 39, 5, 7))
            pygame.draw.rect(superficie, (82, 50, 42), (x - 6, y + 7, 12, 5))
            pygame.draw.line(superficie, (78, 71, 55), (x - 17, y + 18), (x - 14, y + 67), 1)
        pygame.draw.rect(superficie, (86, 64, 51), (0, 215, 23, 117))
        pygame.draw.rect(superficie, (86, 64, 51), (937, 215, 23, 117))
        for y in (232, 258, 284, 310):
            pygame.draw.rect(superficie, (147, 131, 91), (5, y, 13, 3))
            pygame.draw.rect(superficie, (147, 131, 91), (942, y, 13, 3))

    @staticmethod
    def _dibujar_mobiliario(superficie: pygame.Surface, zona: str) -> None:
        # Camilla con sábana arrugada, soporte y ruedas.
        pygame.draw.rect(superficie, (74, 77, 67), (70, 323, 133, 13))
        pygame.draw.rect(superficie, (139, 139, 119), (77, 304, 111, 19))
        pygame.draw.rect(superficie, (174, 166, 140), (88, 307, 43, 7))
        pygame.draw.line(superficie, (33, 39, 36), (86, 336), (86, 363), 4)
        pygame.draw.line(superficie, (33, 39, 36), (184, 336), (184, 363), 4)
        pygame.draw.circle(superficie, (20, 25, 24), (84, 365), 7, 3)
        pygame.draw.circle(superficie, (20, 25, 24), (185, 365), 7, 3)
        pygame.draw.rect(superficie, (91, 78, 62), (797, 316, 72, 40))
        pygame.draw.rect(superficie, (39, 44, 40), (803, 322, 60, 27))
        pygame.draw.circle(superficie, (24, 29, 27), (807, 360), 9, 3)
        pygame.draw.circle(superficie, (24, 29, 27), (860, 360), 9, 3)
        if zona == "sala2":
            pygame.draw.ellipse(superficie, (67, 38, 35), (455, 348, 124, 18))
            pygame.draw.rect(superficie, (106, 89, 65), (415, 293, 114, 30))
            pygame.draw.rect(superficie, (48, 47, 40), (427, 298, 90, 20))

    @staticmethod
    def _crear_grano() -> pygame.Surface:
        grano = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        azar = random.Random(210)
        for _ in range(2600):
            x, y = azar.randrange(ANCHO), azar.randrange(ALTO)
            tono = azar.choice((130, 160, 190))
            grano.set_at((x, y), (tono, tono, tono, azar.randrange(8, 24)))
        return grano

    @staticmethod
    def _crear_vineta() -> pygame.Surface:
        pequena = pygame.Surface((320, 180), pygame.SRCALPHA)
        for y in range(180):
            for x in range(320):
                distancia = max(abs(x - 159.5) / 159.5, abs(y - 89.5) / 89.5)
                intensidad = max(0.0, (distancia - 0.48) / 0.52)
                alpha = int(92 * intensidad * intensidad)
                pequena.set_at((x, y), (0, 0, 0, alpha))
        return pygame.transform.scale(pequena, (ANCHO, ALTO))

    def dibujar_fondo(self, pantalla: pygame.Surface, zona: str, tiempo: float) -> None:
        pantalla.blit(self.fondos[zona], (0, 0))
        brillo = 0.72 + 0.12 * math.sin(tiempo * 7.0) + 0.04 * math.sin(tiempo * 19.0)
        color = (int(121 * brillo), int(136 * brillo), int(108 * brillo))
        for x in (197, 677):
            pygame.draw.rect(pantalla, (30, 34, 31), (x, 34, 86, 19))
            pygame.draw.rect(pantalla, color, (x + 7, 38, 72, 8))

    def aplicar_atmosfera(
        self, pantalla: pygame.Surface, jugadores: list[pygame.Rect], tiempo: float
    ) -> None:
        capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        capa.fill((3, 6, 5, 148))
        for rect in jugadores:
            centro = rect.center
            radio = 145 + int(4 * math.sin(tiempo * 4.0))
            for radio_luz in range(radio, 0, -3):
                proporcion = radio_luz / radio
                alpha = int(138 * proporcion ** 2.2)
                pygame.draw.circle(capa, (4, 5, 4, alpha), centro, radio_luz)
        pantalla.blit(capa, (0, 0))
        pantalla.blit(self.vineta, (0, 0))
        pantalla.blit(self.grano, (0, 0))