"""Cinemática 2: cementerio, chicas de espaldas sobre el cadáver en la tumba final."""

import math
import random
import pygame

from juego.config import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA,
    PALETA_CEMENTERIO,
)
from juego.scenes.base_scene import BaseScene
from juego.systems.audio_ambiente import AudioAmbiente

# =============================================================================
# CONSTANTES CONFIGURABLES DE LA CINEMÁTICA 2 (en segundos)
# =============================================================================
TIEMPO_NEGRO = 3.0
DURACION_CINEMATICA = 7.0
DURACION_FADE = 0.5

# Zoom de cámara (100% al 110% durante la cinemática)
ZOOM_INICIAL = 1.0
ZOOM_FINAL = 1.10

# Resolución interna para estética pixel art retro (320x180 se escala 3x a 960x540)
ANCHO_BUFFER = 320
ALTO_BUFFER = 180


class Cinematica2(BaseScene):
    """Cinemática del cementerio con estética pixel art de terror, iluminación y atmósfera."""

    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        self.tiempo_total = 0.0
        self.etapa = "negro"  # 'negro', 'cinematica', 'terminada'
        self.zoom = ZOOM_INICIAL

        # Canvas pixel art interno de baja resolución
        self.buffer_pixel = pygame.Surface((ANCHO_BUFFER, ALTO_BUFFER))
        self.superficie_pantalla = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))

        # Viñeta y grano animados
        self.vineta_buffer = self._crear_vineta_buffer()
        self.cuadros_grano = self._crear_grano_buffer()

        # Partículas ambientales en suspensión (polvo, niebla, hojas secas)
        self.particulas = self._crear_particulas(48)

        # Sistema de audio con placeholders seguros
        self.audio = AudioAmbiente(
            (
                "viento_cementerio",
                "masticacion_baja",
                "respiracion",
                "tono_grave",
            )
        )
        self._audio_iniciado = False

        # Registro en consola al iniciar
        print(f"[{self.tiempo_total:05.2f}s] Cinemática 2: Inicio etapa NEGRO (duración: {TIEMPO_NEGRO:04.2f}s)")

    # -------------------------------------------------------------------------
    # Generadores de textura y atmósfera
    # -------------------------------------------------------------------------
    @staticmethod
    def _crear_vineta_buffer() -> pygame.Surface:
        """Crea una viñeta oscura suave para los bordes del encuadre interno."""
        vineta = pygame.Surface((ANCHO_BUFFER, ALTO_BUFFER), pygame.SRCALPHA)
        cx, cy = ANCHO_BUFFER / 2.0, ALTO_BUFFER / 2.0
        for y in range(ALTO_BUFFER):
            for x in range(ANCHO_BUFFER):
                dx = (x - cx) / cx
                dy = (y - cy) / cy
                dist = math.sqrt(dx * dx * 0.9 + dy * dy * 1.1)
                if dist > 0.62:
                    fuerza = min(1.0, (dist - 0.62) / 0.55)
                    alpha = min(220, int(220 * (fuerza ** 1.6)))
                    vineta.set_at((x, y), (2, 3, 5, alpha))
        return vineta

    @staticmethod
    def _crear_grano_buffer() -> list[pygame.Surface]:
        """Crea fotogramas de grano fílmico animado."""
        fotogramas = []
        for i in range(4):
            surf = pygame.Surface((ANCHO_BUFFER, ALTO_BUFFER), pygame.SRCALPHA)
            rng = random.Random(900 + i * 43)
            for _ in range(500):
                gx = rng.randrange(ANCHO_BUFFER)
                gy = rng.randrange(ALTO_BUFFER)
                gris = rng.choice((120, 150, 180, 210))
                alpha = rng.randrange(10, 30)
                surf.set_at((gx, gy), (gris, gris, gris, alpha))
            fotogramas.append(surf)
        return fotogramas

    @staticmethod
    def _crear_particulas(cantidad: int) -> list[dict]:
        """Partículas de polvo, niebla y hojas secas suspendidas en el aire."""
        rng = random.Random(2026)
        particulas = []
        for _ in range(cantidad):
            particulas.append(
                {
                    "x": rng.uniform(0, ANCHO_BUFFER),
                    "y": rng.uniform(15, ALTO_BUFFER - 10),
                    "vx": rng.uniform(4.0, 11.0),
                    "vy": rng.uniform(-1.0, 1.8),
                    "osc": rng.uniform(0.6, 2.8),
                    "fase": rng.uniform(0, math.tau),
                    "color": rng.choice(((95, 110, 105), (65, 70, 60), (120, 130, 125))),
                    "tam": rng.choice((1, 1, 2)),
                }
            )
        return particulas

    # -------------------------------------------------------------------------
    # Eventos y actualización
    # -------------------------------------------------------------------------
    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                self._siguiente_escena()
            elif evento.key == pygame.K_F5:
                # Reinicio de depuración
                print("[DEBUG] Reiniciando Cinemática 2.")
                self.tiempo_total = 0.0
                self.etapa = "negro"
                self.zoom = ZOOM_INICIAL
                self._audio_iniciado = False
                print(f"[{self.tiempo_total:05.2f}s] Cinemática 2: Inicio etapa NEGRO (duración: {TIEMPO_NEGRO:04.2f}s)")

    def update(self, delta: float) -> None:
        tiempo_anterior = self.tiempo_total
        self.tiempo_total += delta

        # Transición de etapa NEGRO -> CINEMÁTICA
        if tiempo_anterior < TIEMPO_NEGRO <= self.tiempo_total:
            self.etapa = "cinematica"
            print(
                f"[{self.tiempo_total:05.2f}s] Cinemática 2: Fin etapa NEGRO (duración real: {TIEMPO_NEGRO:04.2f}s). "
                f"Inicio etapa CINEMÁTICA (duración: {DURACION_CINEMATICA:04.2f}s)"
            )
            if not self._audio_iniciado:
                self.audio.reproducir_ambientes(
                    ["viento_cementerio", "masticacion_baja", "respiracion", "tono_grave"]
                )
                self._audio_iniciado = True

        tiempo_fin = TIEMPO_NEGRO + DURACION_CINEMATICA

        # En la cinemática: calcular zoom progresivo y volumen del tono grave
        if self.tiempo_total >= TIEMPO_NEGRO:
            progreso_cine = min(1.0, (self.tiempo_total - TIEMPO_NEGRO) / DURACION_CINEMATICA)
            self.zoom = ZOOM_INICIAL + (ZOOM_FINAL - ZOOM_INICIAL) * progreso_cine

            # Subida suave de volumen en el tono grave
            if "tono_grave" in self.audio.canales:
                volumen_base = 0.35
                self.audio.canales["tono_grave"].set_volume(volumen_base * (0.2 + 0.8 * progreso_cine))

        # Transición al terminar la cinemática
        if self.tiempo_total >= tiempo_fin:
            self._siguiente_escena()

    def _siguiente_escena(self) -> None:
        from juego.scenes.placeholder import SiguienteEscenaPendiente

        duracion_cine = max(0.0, self.tiempo_total - TIEMPO_NEGRO)
        print(
            f"[{self.tiempo_total:05.2f}s] Cinemática 2: Fin etapa CINEMÁTICA "
            f"(duración real: {duracion_cine:04.2f}s). Transición a SIGUIENTE ESCENA"
        )
        self.audio.detener_ambientes()
        self.gestor.start(SiguienteEscenaPendiente)
        self.gestor.estado_fundido = "quieto"
        self.gestor.opacidad = 0

    # -------------------------------------------------------------------------
    # Renderizado
    # -------------------------------------------------------------------------
    def draw(self, pantalla: pygame.Surface) -> None:
        # Etapa 1: PANTALLA TOTALMENTE NEGRA durante TIEMPO_NEGRO (3.0s)
        if self.tiempo_total < TIEMPO_NEGRO:
            pantalla.fill((0, 0, 0))
            return

        # Etapa 2: CINEMÁTICA ACTIVA (3.0s a 10.0s)
        tiempo_cine = self.tiempo_total - TIEMPO_NEGRO

        # 1. Dibujar escena completa en el canvas pixel art (320x180)
        self._dibujar_escena_pixel(self.buffer_pixel, tiempo_cine)

        # 2. Aplicar viñeta y grano en baja resolución
        self.buffer_pixel.blit(self.vineta_buffer, (0, 0))
        idx_grano = int(self.tiempo_total * 8.0) % len(self.cuadros_grano)
        self.buffer_pixel.blit(self.cuadros_grano[idx_grano], (0, 0))

        # 3. Escalar con nearest-neighbor a la resolución nativa (960x540)
        pygame.transform.scale(self.buffer_pixel, (ANCHO_PANTALLA, ALTO_PANTALLA), self.superficie_pantalla)

        # 4. Aplicar acercamiento de cámara (zoom del 100% al 110%)
        if self.zoom > 1.001:
            ancho_zoom = int(ANCHO_PANTALLA * self.zoom)
            alto_zoom = int(ALTO_PANTALLA * self.zoom)
            superficie_zoom = pygame.transform.scale(self.superficie_pantalla, (ancho_zoom, alto_zoom))
            cx = (ancho_zoom - ANCHO_PANTALLA) // 2
            cy = (alto_zoom - ALTO_PANTALLA) // 2
            pantalla.blit(superficie_zoom, (-cx, -cy))
        else:
            pantalla.blit(self.superficie_pantalla, (0, 0))

        # 5. Fundidos de entrada (0.5s) y salida (0.5s)
        alpha_fade = 0
        if tiempo_cine < DURACION_FADE:
            # Fade-in desde negro
            progreso = tiempo_cine / DURACION_FADE
            alpha_fade = int(255 * (1.0 - progreso))
        elif tiempo_cine > (DURACION_CINEMATICA - DURACION_FADE):
            # Fade-out hacia negro
            progreso = (tiempo_cine - (DURACION_CINEMATICA - DURACION_FADE)) / DURACION_FADE
            alpha_fade = min(255, int(255 * progreso))

        if alpha_fade > 0:
            capa_negra = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
            capa_negra.fill((0, 0, 0, alpha_fade))
            pantalla.blit(capa_negra, (0, 0))

    # -------------------------------------------------------------------------
    # Dibujo de la escena en 320x180
    # -------------------------------------------------------------------------
    def _dibujar_escena_pixel(self, surf: pygame.Surface, t: float) -> None:
        """Renderiza todo el arte pixel art con capas de fondo, iluminación y personajes."""
        # 1. Cielo nocturno con gradiente y estrellas
        self._dibujar_cielo(surf, t)

        # 2. Siluetas de árboles secos y lápidas lejanas
        self._dibujar_fondo_lejano(surf)

        # 3. Suelo del cementerio y tumba monumental
        self._dibujar_tumba_y_suelo(surf, t)

        # 4. Niebla baja desplazándose entre las tumbas
        self._dibujar_niebla(surf, t, capa="fondo")

        # 5. Cadáver tendido en el suelo sobre la plataforma de la tumba
        self._dibujar_cadaver(surf)

        # 6. Primer plano: las dos chicas de espaldas sobre el cadáver con movimiento (>= 40% pantalla)
        self._dibujar_chicas_comiendo(surf, t)

        # 7. Niebla frontal y partículas flotantes
        self._dibujar_niebla(surf, t, capa="frente")
        self._dibujar_particulas_aire(surf, t)

        # 8. Parpadeo sutil de luz y ambientación fría
        self._dibujar_iluminacion_ambiental(surf, t)

    def _dibujar_cielo(self, surf: pygame.Surface, t: float) -> None:
        # Gradiente nocturno profundo
        surf.fill((6, 9, 12))
        pygame.draw.rect(surf, (10, 16, 20), (0, 30, ANCHO_BUFFER, 50))
        pygame.draw.rect(surf, (15, 23, 27), (0, 80, ANCHO_BUFFER, 45))

        # Estrellas tenues
        rng = random.Random(404)
        for _ in range(40):
            sx = rng.randrange(ANCHO_BUFFER)
            sy = rng.randrange(4, 70)
            brillo = rng.choice(((50, 60, 58), (75, 90, 85), (100, 115, 108)))
            surf.set_at((sx, sy), brillo)

        # Luna fría con cráteres y resplandor tenue
        lx, ly = 246, 36
        pygame.draw.circle(surf, (18, 28, 32), (lx, ly), 20)  # halo suave
        pygame.draw.circle(surf, PALETA_CEMENTERIO["luna_sombra"], (lx, ly), 15)
        pygame.draw.circle(surf, PALETA_CEMENTERIO["luna"], (lx - 2, ly - 2), 13)
        # Cráteres lunares
        pygame.draw.circle(surf, PALETA_CEMENTERIO["crater"], (lx - 5, ly - 4), 3)
        pygame.draw.circle(surf, PALETA_CEMENTERIO["crater"], (lx + 2, ly + 2), 2)
        pygame.draw.rect(surf, PALETA_CEMENTERIO["crater"], (lx - 1, ly - 7, 3, 2))

    def _dibujar_fondo_lejano(self, surf: pygame.Surface) -> None:
        # Árboles secos y retorcidos
        col_arbol = (14, 20, 20)
        col_arbol_borde = (24, 32, 30)

        # Árbol seco izquierda
        pygame.draw.line(surf, col_arbol, (36, 130), (28, 65), 3)
        pygame.draw.line(surf, col_arbol, (28, 90), (12, 70), 2)
        pygame.draw.line(surf, col_arbol, (28, 76), (44, 60), 2)
        pygame.draw.line(surf, col_arbol_borde, (12, 70), (6, 64), 1)

        # Árbol seco derecha
        pygame.draw.line(surf, col_arbol, (288, 130), (294, 62), 3)
        pygame.draw.line(surf, col_arbol, (291, 92), (276, 75), 2)
        pygame.draw.line(surf, col_arbol, (292, 78), (308, 64), 2)

        # Lápidas y cruces lejanas en silueta
        col_lapida_lej = (20, 26, 25)
        for lx, ly, w, h in ((14, 114, 13, 18), (56, 118, 10, 14), (264, 116, 12, 16), (300, 112, 14, 20)):
            pygame.draw.rect(surf, col_lapida_lej, (lx, ly, w, h))
            pygame.draw.ellipse(surf, col_lapida_lej, (lx, ly - 3, w, 6))

        # Pequeña cruz lejana
        pygame.draw.rect(surf, col_lapida_lej, (78, 106, 4, 24))
        pygame.draw.rect(surf, col_lapida_lej, (73, 112, 14, 3))

    def _dibujar_tumba_y_suelo(self, surf: pygame.Surface, t: float) -> None:
        y_suelo = 132

        # Capa de suelo de tierra y piedra
        pygame.draw.rect(surf, (20, 24, 22), (0, y_suelo, ANCHO_BUFFER, ALTO_BUFFER - y_suelo))
        pygame.draw.line(surf, (32, 40, 36), (0, y_suelo), (ANCHO_BUFFER, y_suelo), 1)
        pygame.draw.line(surf, (12, 15, 14), (0, y_suelo + 1), (ANCHO_BUFFER, y_suelo + 1), 1)

        # Plataforma monumental de la tumba final (piedra gastada con grietas)
        tx, ty, tw, th = 45, 122, 230, 24
        # Sombra proyectada por la tumba
        pygame.draw.ellipse(surf, (6, 8, 8), (tx - 14, ty + th - 6, tw + 28, 16))

        # Bloque de piedra de la tumba
        pygame.draw.rect(surf, (34, 40, 38), (tx, ty, tw, th))
        pygame.draw.rect(surf, (50, 58, 54), (tx + 1, ty + 1, tw - 2, 2))  # borde de luz lunar superior
        pygame.draw.rect(surf, (20, 24, 23), (tx, ty + th - 3, tw, 3))  # sombra base
        pygame.draw.rect(surf, (14, 18, 17), (tx, ty, tw, th), 1)  # contorno oscuro

        # Grietas y marcas antiguas en la losa de piedra
        pygame.draw.line(surf, (14, 18, 17), (tx + 40, ty + 2), (tx + 48, ty + 12), 1)
        pygame.draw.line(surf, (14, 18, 17), (tx + 48, ty + 12), (tx + 54, ty + 18), 1)
        pygame.draw.line(surf, (14, 18, 17), (tx + 175, ty + 3), (tx + 182, ty + 16), 1)

        # Cruz de piedra de fondo en la cabecera de la tumba
        mx = 153
        my = 64
        mw = 14
        mh = 60
        # Sombra proyectada de la cruz
        pygame.draw.rect(surf, (8, 10, 10), (mx + mw, my + 8, 16, mh))
        # Poste vertical de la cruz
        pygame.draw.rect(surf, PALETA_CEMENTERIO["lapida_final"], (mx, my, mw, mh))
        pygame.draw.line(surf, (75, 85, 78), (mx + 1, my), (mx + 1, my + mh), 1)  # luz de luna
        # Travesaño horizontal
        pygame.draw.rect(surf, PALETA_CEMENTERIO["lapida_final"], (mx - 14, my + 16, mw + 28, 11))
        pygame.draw.line(surf, (75, 85, 78), (mx - 14, my + 16), (mx + mw + 14, my + 16), 1)
        # Bordes
        pygame.draw.rect(surf, (16, 20, 18), (mx, my, mw, mh), 1)
        pygame.draw.rect(surf, (16, 20, 18), (mx - 14, my + 16, mw + 28, 11), 1)

    def _dibujar_cadaver(self, surf: pygame.Surface) -> None:
        """Dibuja el cadáver tendido horizontalmente y apoyado sobre la losa de la tumba."""
        cx = 80
        cy = 122
        cw = 160

        # Sombra proyectada directamente debajo del cuerpo sobre la losa de la tumba
        pygame.draw.ellipse(surf, (6, 8, 8), (cx - 6, cy + 9, cw + 12, 9))

        # Cabeza ladeada inerte e inmóvil (a la izquierda)
        pygame.draw.circle(surf, (58, 64, 60), (cx + 12, cy + 5), 7)
        pygame.draw.circle(surf, (14, 16, 15), (cx + 12, cy + 5), 7, 1)
        # Cabello desgreñado pegado a la piedra
        pygame.draw.rect(surf, (14, 15, 14), (cx + 6, cy + 4, 9, 5))

        # Cuello y torso caído con ropa oscura (camisa/chaqueta de sereno)
        pygame.draw.rect(surf, (24, 28, 26), (cx + 18, cy + 2, 60, 11))
        pygame.draw.line(surf, (40, 48, 44), (cx + 19, cy + 2), (cx + 76, cy + 2), 1)

        # Brazo izquierdo inerte colgando sobre el borde de piedra
        pygame.draw.line(surf, (24, 28, 26), (cx + 34, cy + 6), (cx + 34, cy + 18), 3)
        pygame.draw.circle(surf, (58, 64, 60), (cx + 34, cy + 19), 2)  # mano inerte pálida

        # Piernas y pantalones extendidos hacia la derecha
        pygame.draw.rect(surf, (20, 24, 22), (cx + 78, cy + 4, 62, 8))
        # Botas oscuras apoyadas rectas sobre la losa
        pygame.draw.rect(surf, (12, 14, 13), (cx + 138, cy + 2, 14, 11))
        pygame.draw.line(surf, (34, 38, 36), (cx + 138, cy + 2), (cx + 152, cy + 2), 1)

    def _dibujar_chicas_comiendo(self, surf: pygame.Surface, t: float) -> None:
        """
        Dibuja a las dos chicas de espaldas en PRIMER PLANO, ocupando al menos el 40%
        del alto de la pantalla (altura de 82 a 92 px sobre 180 px = 45% a 51% del alto),
        inclinadas sobre el cadáver, con movimiento continuo de devoración.
        """
        # Ritmo de la Chica 1 (Izquierda): más rápida, voraz, con sacudidas y temblor espasmódico
        freq1 = 3.9
        fase1 = t * freq1
        dip_torso_1 = math.sin(fase1) * 4.2 + abs(math.sin(fase1 * 2.0)) * 1.6
        dip_cabeza_1 = math.sin(fase1 - 0.4) * 5.6
        brazo_pull_1 = math.cos(fase1) * 3.2

        # Temblor ocasional en Chica 1
        temblor_1 = 0.0
        if (t % 2.2) < 0.35:
            temblor_1 = math.sin(t * 48.0) * 1.9

        # Ritmo de la Chica 2 (Derecha): más lenta, pesada, inclinación profunda y desgarre sostenido
        freq2 = 2.1
        fase2 = t * freq2 + 1.3
        dip_torso_2 = math.sin(fase2) * 5.8
        dip_cabeza_2 = math.sin(fase2 - 0.65) * 6.5
        sway_2 = math.sin(fase2 * 0.75) * 2.5
        brazo_pull_2 = math.cos(fase2) * 3.8

        c1_x = 114 + temblor_1
        c1_y_base = 180  # Llega hasta el borde inferior de la pantalla

        c2_x = 198 + sway_2
        c2_y_base = 180

        # Sombras proyectadas debajo de las chicas sobre la tumba y el suelo
        pygame.draw.ellipse(surf, (6, 8, 8), (c1_x - 30, c1_y_base - 18, 62, 20))
        pygame.draw.ellipse(surf, (6, 8, 8), (c2_x - 32, c2_y_base - 18, 66, 20))

        # ---------------------------------------------------------------------
        # CHICA 1 (Izquierda): altura total ~86 px (47.8% de la pantalla)
        # ---------------------------------------------------------------------
        # Falda institucional rasgada / base del cuerpo
        falda_pts_1 = [
            (c1_x - 24, c1_y_base),
            (c1_x + 26, c1_y_base),
            (c1_x + 21, c1_y_base - 42),
            (c1_x - 19, c1_y_base - 42),
        ]
        pygame.draw.polygon(surf, (16, 20, 19), falda_pts_1)
        pygame.draw.polygon(surf, (8, 11, 10), falda_pts_1, 1)
        # Pliegues de la falda
        pygame.draw.line(surf, (11, 14, 13), (c1_x - 4, c1_y_base - 40), (c1_x - 6, c1_y_base), 1)
        pygame.draw.line(surf, (11, 14, 13), (c1_x + 10, c1_y_base - 40), (c1_x + 12, c1_y_base), 1)

        # Torso inclinado hacia adelante devorando
        torso_y1 = c1_y_base - 42 + dip_torso_1
        torso_pts_1 = [
            (c1_x - 19, c1_y_base - 42),
            (c1_x + 21, c1_y_base - 42),
            (c1_x + 24, torso_y1 - 32),
            (c1_x - 22, torso_y1 - 30),
        ]
        pygame.draw.polygon(surf, (22, 27, 25), torso_pts_1)
        pygame.draw.polygon(surf, (10, 13, 12), torso_pts_1, 1)

        # Recorte de luz tenue fría en el contorno del hombro y espalda izquierda
        pygame.draw.line(surf, (75, 95, 88), (c1_x - 22, torso_y1 - 30), (c1_x - 19, c1_y_base - 42), 1)

        # Brazos y hombros en movimiento hacia el cadáver
        codo_izq_1 = (c1_x - 30, torso_y1 - 12 + brazo_pull_1)
        mano_izq_1 = (c1_x - 10, torso_y1 + 8 - dip_torso_1 * 0.4)
        pygame.draw.line(surf, (18, 23, 21), (c1_x - 20, torso_y1 - 28), codo_izq_1, 6)
        pygame.draw.line(surf, (18, 23, 21), codo_izq_1, mano_izq_1, 5)

        codo_der_1 = (c1_x + 28, torso_y1 - 10 - brazo_pull_1 * 0.6)
        mano_der_1 = (c1_x + 12, torso_y1 + 9)
        pygame.draw.line(surf, (18, 23, 21), (c1_x + 22, torso_y1 - 30), codo_der_1, 6)
        pygame.draw.line(surf, (18, 23, 21), codo_der_1, mano_der_1, 5)

        # Cabeza que baja y sube en ritmo de mordida
        cabeza_y1 = torso_y1 - 32 + dip_cabeza_1
        cabeza_x1 = c1_x + 1
        pygame.draw.circle(surf, (12, 15, 15), (int(cabeza_x1), int(cabeza_y1)), 13)
        # Cabello largo desgreñado que cae hacia adelante
        for ox, oy, ow, oh in ((-12, -10, 24, 15), (-14, 2, 9, 18), (6, 2, 8, 17), (-4, 8, 10, 16)):
            pygame.draw.ellipse(surf, (8, 10, 11), (cabeza_x1 + ox, cabeza_y1 + oy, ow, oh))
        # Borde de luz lunar en la coronilla
        pygame.draw.arc(surf, (85, 105, 98), (cabeza_x1 - 11, cabeza_y1 - 12, 22, 15), math.pi * 0.2, math.pi * 0.9, 1)

        # ---------------------------------------------------------------------
        # CHICA 2 (Derecha): altura total ~90 px (50% de la pantalla)
        # ---------------------------------------------------------------------
        # Falda institucional / base
        falda_pts_2 = [
            (c2_x - 26, c2_y_base),
            (c2_x + 28, c2_y_base),
            (c2_x + 23, c2_y_base - 44),
            (c2_x - 21, c2_y_base - 44),
        ]
        pygame.draw.polygon(surf, (24, 26, 22), falda_pts_2)
        pygame.draw.polygon(surf, (10, 12, 10), falda_pts_2, 1)
        # Pliegues
        pygame.draw.line(surf, (14, 16, 13), (c2_x - 5, c2_y_base - 42), (c2_x - 7, c2_y_base), 1)
        pygame.draw.line(surf, (14, 16, 13), (c2_x + 11, c2_y_base - 42), (c2_x + 13, c2_y_base), 1)

        # Torso pesado encorvado sobre el cadáver
        torso_y2 = c2_y_base - 44 + dip_torso_2
        torso_pts_2 = [
            (c2_x - 21, c2_y_base - 44),
            (c2_x + 23, c2_y_base - 44),
            (c2_x + 26, torso_y2 - 35),
            (c2_x - 24, torso_y2 - 33),
        ]
        pygame.draw.polygon(surf, (28, 30, 26), torso_pts_2)
        pygame.draw.polygon(surf, (12, 14, 11), torso_pts_2, 1)

        # Recorte de luz lunar tenue en el hombro derecho
        pygame.draw.line(surf, (85, 100, 88), (c2_x + 26, torso_y2 - 35), (c2_x + 23, c2_y_base - 44), 1)

        # Brazos con hombros curvados hacia adentro despegando trozos
        codo_izq_2 = (c2_x - 32, torso_y2 - 14 - brazo_pull_2 * 0.5)
        mano_izq_2 = (c2_x - 14, torso_y2 + 10)
        pygame.draw.line(surf, (22, 24, 20), (c2_x - 22, torso_y2 - 31), codo_izq_2, 7)
        pygame.draw.line(surf, (22, 24, 20), codo_izq_2, mano_izq_2, 5)

        codo_der_2 = (c2_x + 32, torso_y2 - 10 + brazo_pull_2)
        mano_der_2 = (c2_x + 8, torso_y2 + 11)
        pygame.draw.line(surf, (20, 22, 18), (c2_x + 24, torso_y2 - 33), codo_der_2, 7)
        pygame.draw.line(surf, (20, 22, 18), codo_der_2, mano_der_2, 5)

        # Cabeza encorvada profundamente
        cabeza_y2 = torso_y2 - 35 + dip_cabeza_2
        cabeza_x2 = c2_x - 2
        pygame.draw.circle(surf, (13, 14, 13), (int(cabeza_x2), int(cabeza_y2)), 14)
        # Cabello largo y desgreñado
        for ox, oy, ow, oh in ((-13, -11, 26, 17), (-15, 2, 10, 19), (6, 2, 10, 18), (-5, 9, 11, 16)):
            pygame.draw.ellipse(surf, (9, 10, 9), (cabeza_x2 + ox, cabeza_y2 + oy, ow, oh))
        # Recorte de luz lunar
        pygame.draw.arc(surf, (90, 105, 92), (cabeza_x2 - 12, cabeza_y2 - 13, 24, 16), math.pi * 0.1, math.pi * 0.8, 1)

    def _dibujar_niebla(self, surf: pygame.Surface, t: float, capa: str) -> None:
        """Niebla animada que se desplaza suavemente a diferentes velocidades."""
        niebla_surf = pygame.Surface((ANCHO_BUFFER, ALTO_BUFFER), pygame.SRCALPHA)
        color_niebla = PALETA_CEMENTERIO["niebla"]

        if capa == "fondo":
            # Niebla lejana sobre el suelo del cementerio
            vel = 5.0
            despl = (t * vel) % ANCHO_BUFFER
            for offset in (0, ANCHO_BUFFER):
                nx = -despl + offset
                pygame.draw.ellipse(niebla_surf, (*color_niebla, 16), (nx - 40, 114, 200, 20))
                pygame.draw.ellipse(niebla_surf, (*color_niebla, 14), (nx + 100, 120, 220, 22))
        else:
            # Niebla cercana flotando al pie de las figuras
            vel = 10.0
            despl = (t * vel) % ANCHO_BUFFER
            for offset in (0, ANCHO_BUFFER):
                nx = -despl + offset
                pygame.draw.ellipse(niebla_surf, (*color_niebla, 22), (nx + 10, 150, 230, 26))
                pygame.draw.ellipse(niebla_surf, (*color_niebla, 16), (nx + 170, 158, 180, 24))

        surf.blit(niebla_surf, (0, 0))

    def _dibujar_particulas_aire(self, surf: pygame.Surface, t: float) -> None:
        """Dibuja partículas de polvo y hojas secas flotando en el aire."""
        for p in self.particulas:
            px = int((p["x"] + t * p["vx"]) % ANCHO_BUFFER)
            py = int((p["y"] + math.sin(t * p["osc"] + p["fase"]) * 5.0 + t * p["vy"]) % ALTO_BUFFER)
            pygame.draw.rect(surf, p["color"], (px, py, p["tam"], p["tam"]))

    def _dibujar_iluminacion_ambiental(self, surf: pygame.Surface, t: float) -> None:
        """Parpadeo tenue y tinte frío de atmósfera nocturna."""
        flicker = math.sin(t * 3.2) * 0.03 + math.sin(t * 8.5) * 0.02
        alpha_luz = max(0, min(35, int(18 + flicker * 80)))

        luz_surf = pygame.Surface((ANCHO_BUFFER, ALTO_BUFFER), pygame.SRCALPHA)
        luz_surf.fill((60, 85, 95, alpha_luz))
        surf.blit(luz_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
