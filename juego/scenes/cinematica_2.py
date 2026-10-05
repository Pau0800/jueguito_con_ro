"""Cinemática 2: cementerio, chicas de espaldas y cadáver parcialmente oculto."""

import math
import random

import pygame

from juego.config import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA,
    CINEMATICA_2_FADE_SEGUNDOS,
    CINEMATICA_2_TIEMPO_CINEMATICA,
    CINEMATICA_2_TIEMPO_NEGRO,
    CINEMATICA_2_VELOCIDAD_ANIMACION,
    CINEMATICA_2_VELOCIDAD_TEMBLOR,
    CINEMATICA_2_ZOOM_FINAL,
    CINEMATICA_2_ZOOM_INICIAL,
    PALETA_CEMENTERIO,
    SALTAR_CINEMATICA_HABILITADO,
    TECLA_SALTAR_CINEMATICA,
)
from juego.scenes.base_scene import BaseScene


class Cinematica2(BaseScene):
    """Escena con negro, cinemática de 7 segundos y salida hacia la siguiente escena."""

    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        self.tiempo_total = 0.0
        self.zoom = CINEMATICA_2_ZOOM_INICIAL
        self.opacidad_negra = 255
        self.particulas = self._generar_particulas()
        self.chicas = [
            {"superficie": self._crear_silueta_chica(0), "x": 275, "y": 245},
            {"superficie": self._crear_silueta_chica(1), "x": 510, "y": 250},
        ]
        self.cadaver = self._crear_cadaver_placeholder()
        self._sonidos_placeholder = (
            "viento_cementerio",
            "masticacion_baja",
            "respiracion",
            "tono_grave",
        )
        self._audio_avisado = False

    def handle_event(self, evento: pygame.event.Event) -> None:
        if (
            SALTAR_CINEMATICA_HABILITADO
            and evento.type == pygame.KEYDOWN
            and evento.key == pygame.key.key_code(TECLA_SALTAR_CINEMATICA)
        ):
            self._siguiente_escena()
            return
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
            self._siguiente_escena()

    def update(self, delta: float) -> None:
        self.tiempo_total += delta
        self._actualizar_zoom()
        self._actualizar_sonidos_placeholder()
        if self.tiempo_total >= self._duracion_total():
            self._siguiente_escena()

    def draw(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((7, 9, 11))
        if self.tiempo_total <= CINEMATICA_2_TIEMPO_NEGRO:
            self.opacidad_negra = 255
            self._dibujar_fondo(pantalla)
            self._dibujar_overlay_negro(pantalla, self.opacidad_negra)
            return

        if self.tiempo_total <= CINEMATICA_2_TIEMPO_NEGRO + CINEMATICA_2_FADE_SEGUNDOS:
            progreso = (self.tiempo_total - CINEMATICA_2_TIEMPO_NEGRO) / CINEMATICA_2_FADE_SEGUNDOS
            self.opacidad_negra = int(255 * (1.0 - progreso))
            self._dibujar_fondo(pantalla)
            self._dibujar_elementos_cinematica(pantalla)
            self._dibujar_overlay_negro(pantalla, self.opacidad_negra)
            return

        if self.tiempo_total <= self._duracion_cinematica_total():
            self.opacidad_negra = 0
            self._dibujar_fondo(pantalla)
            self._dibujar_elementos_cinematica(pantalla)
            self._dibujar_vineta(pantalla)
            return

        if self.tiempo_total <= self._duracion_cinematica_total() + CINEMATICA_2_FADE_SEGUNDOS:
            progreso = (self.tiempo_total - self._duracion_cinematica_total()) / CINEMATICA_2_FADE_SEGUNDOS
            self.opacidad_negra = int(255 * progreso)
            self._dibujar_fondo(pantalla)
            self._dibujar_elementos_cinematica(pantalla)
            self._dibujar_overlay_negro(pantalla, self.opacidad_negra)
            return

        self._dibujar_overlay_negro(pantalla, 255)

    def _duracion_cinematica_total(self) -> float:
        return CINEMATICA_2_TIEMPO_NEGRO + CINEMATICA_2_FADE_SEGUNDOS + CINEMATICA_2_TIEMPO_CINEMATICA

    def _duracion_total(self) -> float:
        return self._duracion_cinematica_total() + CINEMATICA_2_FADE_SEGUNDOS

    def _siguiente_escena(self) -> None:
        from juego.scenes.placeholder import Cinematica3Pendiente

        print("Cinemática 2: transicion a la siguiente escena del juego.")
        print("Cinemática 3 pendiente: falta implementar la escena de continuación.")
        self.gestor.change_scene(Cinematica3Pendiente)

    def _actualizar_zoom(self) -> None:
        if self.tiempo_total <= CINEMATICA_2_TIEMPO_NEGRO:
            self.zoom = CINEMATICA_2_ZOOM_INICIAL
            return
        if self.tiempo_total <= self._duracion_cinematica_total():
            progreso = min(1.0, (self.tiempo_total - CINEMATICA_2_TIEMPO_NEGRO) / max(CINEMATICA_2_TIEMPO_CINEMATICA, 0.1))
            self.zoom = CINEMATICA_2_ZOOM_INICIAL + (CINEMATICA_2_ZOOM_FINAL - CINEMATICA_2_ZOOM_INICIAL) * progreso
        else:
            self.zoom = CINEMATICA_2_ZOOM_FINAL

    def _actualizar_sonidos_placeholder(self) -> None:
        if self._audio_avisado:
            return
        if self.tiempo_total >= CINEMATICA_2_TIEMPO_NEGRO:
            print("Cinemática 2: placeholders de audio preparados ->", self._sonidos_placeholder)
            self._audio_avisado = True

    def _dibujar_fondo(self, pantalla: pygame.Surface) -> None:
        superficie = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        superficie.fill((9, 13, 15, 255))

        pygame.draw.rect(superficie, (15, 20, 22), (0, 0, ANCHO_PANTALLA, 260))
        pygame.draw.circle(superficie, PALETA_CEMENTERIO["luna"], (760, 92), 52)
        pygame.draw.circle(superficie, PALETA_CEMENTERIO["luna_sombra"], (778, 105), 16)

        for x in (70, 200, 330, 520, 690, 850):
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["piedra"], (x, 282, 28, 74))
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["grabado"], (x + 7, 296, 14, 44), 2)
        for x in (110, 260, 470, 720):
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol"], (x, 315), (x - 18, 250), 5)
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol"], (x + 8, 280), (x + 32, 245), 4)

        pygame.draw.rect(superficie, (25, 28, 29), (0, 340, ANCHO_PANTALLA, ALTO_PANTALLA - 340))
        for x in range(-18, ANCHO_PANTALLA + 40, 90):
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["fondo_piedra"], (x, 360, 24, 150))

        # Brillo lunar lateral para recortar siluetas.
        sombra = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        luz = pygame.Rect(260, 100, 400, 300)
        pygame.draw.ellipse(sombra, (0, 0, 0, 115), luz)
        superficie.blit(sombra, (0, 0))

        if abs(self.zoom - 1.0) > 0.001:
            render = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
            render.blit(superficie, (0, 0))
            escala = pygame.transform.smoothscale(render, (int(ANCHO_PANTALLA * self.zoom), int(ALTO_PANTALLA * self.zoom)))
            rect = escala.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
            superficie = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
            superficie.blit(escala, rect)

        pantalla.blit(superficie, (0, 0))

    def _dibujar_elementos_cinematica(self, pantalla: pygame.Surface) -> None:
        tumba_x = 350
        tumba_y = 420
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["plataforma_final"], (tumba_x - 18, tumba_y - 8, 260, 22))
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["lapida_final"], (tumba_x + 56, tumba_y - 112, 56, 108))
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["lapida_final_linea"], (tumba_x + 82, tumba_y - 92, 4, 90), 2)

        # Cuerpo del cadáver tendido en el suelo, oculto parcialmente por las chicas.
        cadaver_x = tumba_x + 118
        cadaver_y = tumba_y - 40
        pantalla.blit(self.cadaver, (cadaver_x, cadaver_y))

        for indice, chica in enumerate(self.chicas):
            offset_x = math.sin(self.tiempo_total * (0.9 + indice * 0.25) * CINEMATICA_2_VELOCIDAD_ANIMACION) * (5.0 if indice == 0 else 6.0)
            offset_y = math.cos(self.tiempo_total * (1.1 + indice * 0.35) * CINEMATICA_2_VELOCIDAD_ANIMACION) * (3.0 if indice == 0 else 4.0)
            x = int(chica["x"] + offset_x + (self.tiempo_total * 0.2 if indice == 1 else 0.0))
            y = int(chica["y"] + offset_y + (math.sin(self.tiempo_total * 2.2) * 2.5 if indice == 1 else 0.0))
            pantalla.blit(chica["superficie"], (x, y))

        self._dibujar_particulas(pantalla)
        self._dibujar_niebla(pantalla)

    def _dibujar_particulas(self, pantalla: pygame.Surface) -> None:
        for particula in self.particulas:
            x = int((particula[0] + self.tiempo_total * particula[3] * 9.0) % ANCHO_PANTALLA)
            y = int((particula[1] + self.tiempo_total * particula[5] * 18.0) % ALTO_PANTALLA)
            pygame.draw.rect(pantalla, particula[2], (x, y, 2, 2))

    def _dibujar_niebla(self, pantalla: pygame.Surface) -> None:
        for indice, desplazamiento in enumerate((0, 135, 300, 460)):
            rect = pygame.Rect(
                int((self.tiempo_total * (12 + indice * 6) + desplazamiento) % (ANCHO_PANTALLA + 140)) - 70,
                180 + indice * 52,
                ANCHO_PANTALLA + 140,
                80,
            )
            pygame.draw.ellipse(pantalla, (*PALETA_CEMENTERIO["niebla"], 24 + indice * 10), rect)

    def _dibujar_overlay_negro(self, pantalla: pygame.Surface, alpha: int) -> None:
        capa = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        capa.fill((4, 7, 10, alpha))
        pantalla.blit(capa, (0, 0))

    def _dibujar_vineta(self, pantalla: pygame.Surface) -> None:
        sombra = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
        for y in range(ALTO_PANTALLA):
            for x in range(ANCHO_PANTALLA):
                distancia = max(abs(x - ANCHO_PANTALLA / 2) / (ANCHO_PANTALLA / 2), abs(y - ALTO_PANTALLA / 2) / (ALTO_PANTALLA / 2))
                densidad = max(0.0, (distancia - 0.52) / 0.48)
                alpha = int(120 * densidad * densidad)
                if alpha:
                    sombra.set_at((x, y), (0, 0, 0, alpha))
        pantalla.blit(sombra, (0, 0))

    @staticmethod
    def _crear_cadaver_placeholder() -> pygame.Surface:
        superficie = pygame.Surface((120, 62), pygame.SRCALPHA)
        pygame.draw.ellipse(superficie, (28, 27, 27, 200), (5, 10, 80, 28))
        pygame.draw.rect(superficie, (28, 27, 27, 200), (18, 24, 62, 20))
        pygame.draw.rect(superficie, (18, 18, 18, 170), (28, 42, 14, 18))
        pygame.draw.rect(superficie, (18, 18, 18, 170), (58, 42, 14, 18))
        pygame.draw.ellipse(superficie, (10, 12, 12, 170), (8, 18, 26, 10))
        pygame.draw.ellipse(superficie, (10, 12, 12, 170), (56, 18, 26, 10))
        return superficie

    @staticmethod
    def _crear_silueta_chica(indice: int) -> pygame.Surface:
        ancho, alto = 150, 190
        silueta = pygame.Surface((ancho, alto), pygame.SRCALPHA)

        pygame.draw.ellipse(silueta, (15, 17, 19, 220), (52, 8, 38, 28))
        pygame.draw.ellipse(silueta, (18, 18, 18, 220), (48, 4, 46, 24))

        pygame.draw.rect(silueta, (20, 23, 24, 230), (40, 30, 18, 72))
        pygame.draw.rect(silueta, (20, 23, 24, 230), (82, 30, 18, 72))
        pygame.draw.rect(silueta, (16, 17, 18, 220), (35, 96, 16, 56))
        pygame.draw.rect(silueta, (16, 17, 18, 220), (93, 96, 16, 56))
        pygame.draw.rect(silueta, (24, 30, 32, 220), (62, 54, 24, 74))

        if indice == 0:
            pygame.draw.ellipse(silueta, (12, 12, 15, 220), (12, 64, 32, 18))
            pygame.draw.ellipse(silueta, (12, 12, 15, 220), (98, 64, 32, 18))
        else:
            pygame.draw.ellipse(silueta, (12, 12, 15, 220), (6, 80, 28, 18))
            pygame.draw.ellipse(silueta, (12, 12, 15, 220), (104, 82, 28, 18))

        pygame.draw.line(silueta, (30, 32, 34, 220), (60, 62), (42, 92), 3)
        pygame.draw.line(silueta, (30, 32, 34, 220), (84, 62), (108, 92), 3)

        sombra = pygame.Surface((ancho, 26), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 110), (7, 0, ancho - 14, 22))
        silueta.blit(sombra, (0, 150))
        return silueta

    @staticmethod
    def _generar_particulas() -> list[tuple[float, float, tuple[int, int, int], float, float]]:
        azar = random.Random(78)
        particulas = []
        for _ in range(90):
            particulas.append(
                (
                    float(azar.randrange(0, ANCHO_PANTALLA)),
                    float(azar.randrange(150, ALTO_PANTALLA)),
                    (100, 110, 105),
                    float(azar.uniform(0.2, 0.9)),
                    float(azar.uniform(0.1, 0.6)),
                )
            )
        return particulas
