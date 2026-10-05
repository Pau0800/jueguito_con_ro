"""Capas de habitación y efectos precalculados para escenas cinematográficas."""

import math
import random
from pathlib import Path

import pygame

from juego.config import CAPAS_HABITACION, EFECTOS_CINEMATICA, PALETA_TERROR, RESOLUCION_INTERNA
from juego.systems.assets import CARGADOR_ASSETS


ANCHO, ALTO = RESOLUCION_INTERNA


class CinematicRoomRenderer:
    """Render pixel art de habitación con caches de fondos, luz y efectos."""

    def __init__(self, datos_habitacion: dict[str, object]) -> None:
        self.datos = datos_habitacion
        self.capas = self._crear_capas()
        rutas_capas = datos_habitacion.get("capas", {})
        for nombre, ruta in rutas_capas.items():
            imagen = CARGADOR_ASSETS.imagen(str(ruta), alpha=str(nombre) != "pared")
            if imagen is not None:
                self.capas[str(nombre)] = pygame.transform.scale(imagen, (ANCHO, ALTO))
        self.vineta = self._crear_vineta()
        self.granos = self._crear_granos()
        self.mascaras_luz = self._crear_mascaras_luz()
        self.tiempo = 0.0
        self.capa_oscura = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self.capa_luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    def _crear_capas(self) -> dict[str, pygame.Surface]:
        pared = pygame.Surface((ANCHO, ALTO))
        pared.fill(PALETA_TERROR["pared"])
        piso = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        props = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        azar = random.Random(304)

        # Baldosas con desgaste, manchas y juntas irregulares.
        pygame.draw.rect(piso, PALETA_TERROR["piso"], (0, 318, ANCHO, ALTO - 318))
        for fila, y in enumerate(range(331, ALTO, 39)):
            corrimiento = 0 if fila % 2 else 32
            pygame.draw.line(piso, (51, 54, 46), (0, y), (ANCHO, y), 2)
            for x in range(corrimiento, ANCHO, 64):
                pygame.draw.line(piso, (50, 53, 46), (x, y), (x, min(y + 39, ALTO)), 2)
        for _ in range(520):
            x, y = azar.randrange(ANCHO), azar.randrange(324, ALTO)
            tono = azar.choice(((33, 38, 35), (57, 55, 44), (67, 55, 45), (43, 49, 42)))
            pygame.draw.rect(piso, tono, (x, y, azar.randrange(2, 13), azar.randrange(1, 5)))
        for x, y, radio_x, radio_y in ((348, 452, 82, 24), (705, 376, 54, 20), (137, 501, 66, 18)):
            pygame.draw.ellipse(piso, (54, 40, 34), (x, y, radio_x, radio_y))
            pygame.draw.ellipse(piso, (77, 50, 39), (x + 12, y + 6, radio_x - 22, radio_y - 11))

        # Descascarado, humedad, grietas y zócalo en la pared.
        for x, y, ancho, alto in (
            (34, 45, 126, 41), (286, 214, 63, 28), (570, 77, 109, 32),
            (700, 253, 82, 31), (873, 120, 54, 45), (220, 270, 43, 19),
        ):
            pygame.draw.rect(pared, PALETA_TERROR["humedad"], (x, y, ancho, alto))
            pygame.draw.rect(pared, PALETA_TERROR["pared_clara"], (x + 5, y + 5, ancho - 16, max(4, alto // 3)))
            pygame.draw.rect(pared, PALETA_TERROR["pared"], (x + 12, y + alto // 2, ancho - 21, max(3, alto // 4)))
        for puntos in (
            ((356, 21), (367, 59), (350, 91), (374, 137)),
            ((618, 188), (607, 216), (626, 245), (614, 285)),
            ((50, 218), (69, 236), (61, 262), (83, 279)),
        ):
            pygame.draw.lines(pared, PALETA_TERROR["sombra"], False, puntos, 4)
            pygame.draw.lines(pared, PALETA_TERROR["pared_clara"], False, tuple((x + 2, y) for x, y in puntos), 1)
        pygame.draw.rect(pared, (24, 30, 28), (0, 306, ANCHO, 17))
        pygame.draw.rect(pared, (111, 89, 62), (0, 306, ANCHO, 3))
        pygame.draw.rect(pared, (61, 53, 43), (0, 322, ANCHO, 4))

        self._dibujar_props_fondo(props)
        return {"pared": pared, "piso": piso, "props": props}

    def _dibujar_props_fondo(self, superficie: pygame.Surface) -> None:
        metal = PALETA_TERROR["metal"]
        madera = PALETA_TERROR["madera"]
        luz = PALETA_TERROR["luz"]
        # Ventana enrejada y vidrio sucio.
        ventana = pygame.Rect(63, 75, 176, 112)
        pygame.draw.rect(superficie, (18, 24, 23), ventana.inflate(12, 12))
        pygame.draw.rect(superficie, madera, ventana, 6)
        pygame.draw.rect(superficie, (43, 63, 58), ventana.inflate(-12, -12))
        for x in range(95, 230, 34):
            pygame.draw.rect(superficie, (25, 34, 32), (x, 77, 5, 108))
            pygame.draw.rect(superficie, (89, 70, 49), (x + 1, 90, 2, 23))
        pygame.draw.rect(superficie, (24, 32, 30), (66, 128, 170, 5))
        pygame.draw.rect(superficie, (94, 83, 61), (71, 82, 23, 28))

        # Cuadros torcidos, placas médicas y un cartel viejo manchado.
        self._cuadro(superficie, pygame.Rect(282, 91, 79, 61), -5)
        self._cuadro(superficie, pygame.Rect(527, 105, 70, 52), 4)
        pygame.draw.rect(superficie, (91, 42, 38), (641, 112, 107, 44))
        pygame.draw.rect(superficie, (50, 41, 34), (647, 118, 95, 32), 2)
        for x in range(656, 734, 12):
            pygame.draw.line(superficie, (156, 137, 99), (x, 124), (x + 4, 124), 2)
        pygame.draw.rect(superficie, (143, 130, 99), (677, 136, 29, 3))

        # Fluorescentes envejecidos sobre el sector de la puerta.
        for x, ancho in ((337, 124), (782, 93)):
            pygame.draw.rect(superficie, (22, 27, 25), (x - 8, 27, ancho + 16, 23))
            pygame.draw.rect(superficie, (72, 82, 69), (x - 3, 31, ancho + 6, 13))
            pygame.draw.rect(superficie, luz, (x, 35, ancho, 5))
            pygame.draw.rect(superficie, (27, 30, 27), (x - 13, 47, 8, 5))
            pygame.draw.rect(superficie, (27, 30, 27), (x + ancho + 5, 47, 8, 5))
            pygame.draw.line(superficie, (184, 177, 132), (x + 13, 37), (x + ancho - 17, 37), 1)

        # Radiador oxidado, mueble bajo, frascos, sábanas y objetos caídos.
        pygame.draw.rect(superficie, (53, 57, 51), (54, 249, 205, 57))
        pygame.draw.rect(superficie, (102, 74, 52), (49, 244, 215, 9))
        for x in range(65, 251, 22):
            pygame.draw.rect(superficie, (73, 72, 60), (x, 257, 11, 43))
            pygame.draw.line(superficie, (119, 84, 57), (x + 2, 258), (x + 2, 295), 2)
        pygame.draw.rect(superficie, (63, 49, 40), (280, 276, 94, 30))
        pygame.draw.rect(superficie, (103, 76, 52), (274, 269, 106, 9))
        pygame.draw.rect(superficie, (29, 34, 31), (289, 285, 19, 21))
        pygame.draw.rect(superficie, (100, 67, 47), (316, 281, 12, 25))
        pygame.draw.ellipse(superficie, (142, 125, 94), (344, 296, 33, 11))
        pygame.draw.polygon(superficie, (118, 97, 68), ((711, 363), (754, 350), (766, 356), (727, 376)))
        pygame.draw.rect(superficie, (78, 56, 44), (171, 456, 38, 14))
        pygame.draw.rect(superficie, (151, 140, 114), (182, 451, 21, 7))
        pygame.draw.line(superficie, metal, (206, 455), (225, 469), 3)

        # Cama oxidada al costado, dejando el centro libre para los actores.
        pygame.draw.ellipse(superficie, (23, 28, 25), (37, 394, 286, 39))
        pygame.draw.rect(superficie, (51, 56, 50), (49, 368, 246, 19))
        pygame.draw.rect(superficie, (141, 139, 118), (61, 351, 223, 20))
        pygame.draw.rect(superficie, (171, 162, 137), (73, 354, 72, 7))
        pygame.draw.line(superficie, (85, 89, 77), (75, 388), (75, 424), 5)
        pygame.draw.line(superficie, (85, 89, 77), (274, 388), (274, 424), 5)
        pygame.draw.circle(superficie, (22, 25, 24), (72, 426), 10, 3)
        pygame.draw.circle(superficie, (22, 25, 24), (276, 426), 10, 3)

    @staticmethod
    def _cuadro(superficie: pygame.Surface, rect: pygame.Rect, inclinacion: int) -> None:
        pygame.draw.rect(superficie, (28, 30, 27), rect.inflate(9, 9))
        pygame.draw.rect(superficie, (117, 91, 58), rect, 4)
        pygame.draw.rect(superficie, (46, 58, 51), rect.inflate(-9, -9))
        pygame.draw.line(superficie, (92, 94, 75), rect.topleft, rect.bottomright, 2)
        pygame.draw.line(superficie, (33, 38, 34), rect.topright, rect.bottomleft, 2)
        pygame.draw.line(superficie, (165, 149, 108), (rect.x + 7, rect.y + 5 + inclinacion), (rect.right - 9, rect.y + 8), 2)

    def _crear_vineta(self) -> pygame.Surface:
        pequena = pygame.Surface((320, 180), pygame.SRCALPHA)
        intensidad_max = float(EFECTOS_CINEMATICA["vineta_intensidad"])
        for y in range(180):
            for x in range(320):
                distancia = max(abs(x - 159.5) / 159.5, abs(y - 89.5) / 89.5)
                fuerza = max(0.0, (distancia - 0.42) / 0.58)
                alfa = round(205 * intensidad_max * fuerza * fuerza)
                pequena.set_at((x, y), (3, 5, 4, alfa))
        return pygame.transform.scale(pequena, (ANCHO, ALTO))

    def _crear_granos(self) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        intensidad = float(EFECTOS_CINEMATICA["grano_intensidad"])
        for semilla in range(4):
            grano = pygame.Surface((320, 180), pygame.SRCALPHA)
            azar = random.Random(3040 + semilla)
            for _ in range(1750):
                x, y = azar.randrange(320), azar.randrange(180)
                alfa = azar.randrange(9, 52)
                tono = azar.choice((109, 143, 177, 203))
                grano.set_at((x, y), (tono, tono, tono, round(alfa * intensidad * 4.0)))
            frames.append(pygame.transform.scale(grano, (ANCHO, ALTO)))
        return frames

    def _crear_mascaras_luz(self) -> list[pygame.Surface]:
        centros = [tuple(EFECTOS_CINEMATICA["luz_puerta_posicion"])]
        for actor in self.datos["characters"]:
            centros.append((int(actor["x"]) + int(actor["width"]) // 2, int(actor["y"]) + int(actor["height"]) // 2))
        mascaras = []
        for indice, centro in enumerate(centros):
            radio = int(EFECTOS_CINEMATICA["luz_puerta_radio"] if indice == 0 else EFECTOS_CINEMATICA["halo_radio"])
            intensidad = float(EFECTOS_CINEMATICA["luz_puerta_intensidad"] if indice == 0 else EFECTOS_CINEMATICA["halo_intensidad"])
            mascara = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            for radio_actual in range(radio, 0, -4):
                distancia = radio_actual / radio
                alfa = round(255 * intensidad * (1 - distancia) ** 1.7)
                pygame.draw.circle(mascara, (0, 0, 0, alfa), centro, radio_actual)
            mascaras.append(mascara)
        return mascaras

    def dibujar_fondo(self, pantalla: pygame.Surface) -> None:
        for nombre in CAPAS_HABITACION:
            if nombre in self.capas:
                pantalla.blit(self.capas[nombre], (0, 0))

    def dibujar_sombras(self, pantalla: pygame.Surface, actores: list[dict[str, object]]) -> None:
        if not EFECTOS_CINEMATICA["sombras_habilitadas"]:
            return
        sombra = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        for actor in actores:
            if not actor["visible"]:
                continue
            x, y = int(actor["x"]), int(actor["y"])
            ancho = int(actor["width"])
            pygame.draw.ellipse(sombra, (4, 5, 4, 142), (x - 8, y + int(actor["height"]) - 9, ancho + 16, 17))
        pygame.draw.ellipse(sombra, (3, 5, 4, 110), (36, 402, 292, 35))
        pantalla.blit(sombra, (0, 0))

    def dibujar_iluminacion_y_efectos(self, pantalla: pygame.Surface, tiempo: float) -> None:
        self.tiempo = tiempo
        if EFECTOS_CINEMATICA["iluminacion_habilitada"]:
            alfa = int(EFECTOS_CINEMATICA["oscuridad_alpha"])
            if EFECTOS_CINEMATICA["parpadeo_habilitado"]:
                frecuencia = float(EFECTOS_CINEMATICA["parpadeo_frecuencia"])
                intensidad = float(EFECTOS_CINEMATICA["parpadeo_intensidad"])
                modulacion = 1.0 + intensidad * math.sin(self.tiempo * frecuencia * math.tau)
                alfa = max(0, min(230, round(alfa / modulacion)))
            self.capa_oscura.fill((7, 9, 8, alfa))
            self.capa_luz.fill((0, 0, 0, 0))
            if EFECTOS_CINEMATICA["luz_puerta_habilitada"]:
                self.capa_luz.blit(self.mascaras_luz[0], (0, 0))
            if EFECTOS_CINEMATICA["halo_personajes_habilitado"]:
                for mascara in self.mascaras_luz[1:]:
                    self.capa_luz.blit(mascara, (0, 0))
            self.capa_oscura.blit(self.capa_luz, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            pantalla.blit(self.capa_oscura, (0, 0))

        if EFECTOS_CINEMATICA["vineta_habilitada"]:
            pantalla.blit(self.vineta, (0, 0))
        if EFECTOS_CINEMATICA["grano_habilitado"]:
            fps_grano = max(1.0, float(EFECTOS_CINEMATICA["grano_fps"]))
            indice = int(self.tiempo * fps_grano) % len(self.granos)
            pantalla.blit(self.granos[indice], (0, 0))

    def cargar_capa_externa(self, nombre: str) -> pygame.Surface | None:
        """Permite sustituir una capa procedural por un PNG con el mismo nombre."""
        ruta = Path("images/cinematics/room_304") / f"{nombre}.png"
        return CARGADOR_ASSETS.imagen(str(ruta), alpha=True)
