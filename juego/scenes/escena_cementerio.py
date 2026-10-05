"""Escena lateral del cementerio, separada del flujo del hospital."""

import json
import math
import random
from pathlib import Path

import pygame

from juego import estado_juego
from juego.config import (
    ALTO_PANTALLA,
    ALTURA_SUELO_CEMENTERIO,
    ANCHO_PANTALLA,
    CANTIDAD_TUMBAS_ABIERTAS_CEMENTERIO,
    CAPAS_CEMENTERIO,
    DISTANCIA_RESCATE,
    DURACION_CARTEL_ADVERTENCIA_CEMENTERIO,
    EFECTOS_CEMENTERIO,
    INTERVALO_PASOS_CEMENTERIO,
    LARGO_NIVEL_CEMENTERIO,
    MARGEN_CAMARA_CEMENTERIO,
    PALETA_CEMENTERIO,
    SEGUNDOS_FINAL_CEMENTERIO,
    SEGUNDOS_RESCATE,
    SEGUNDOS_FADE_INTRO_CEMENTERIO,
    SILUETAS_FINALES_CEMENTERIO,
    TOQUES_RESCATE_NECESARIOS,
    VELOCIDAD_CAMARA_CEMENTERIO,
)
from juego.scenes.base_scene import BaseScene
from juego.systems.audio_ambiente import AudioAmbiente
from juego.systems.dialogue import DialogueBox
from juego.systems.fonts import cargar_fuente
from juego.systems.player_cementerio import JugadorCementerio
from juego.systems.assets import CARGADOR_ASSETS

class CamaraCementerio:
    """Mantiene al grupo en pantalla y limita el paneo al largo del nivel."""

    def __init__(self) -> None:
        self.x = 0.0

    def actualizar(self, jugadores: list[JugadorCementerio], delta: float) -> None:
        centros = [jugador.rect.centerx for jugador in jugadores]
        centro_grupo = (min(centros) + max(centros)) / 2
        objetivo = centro_grupo - ANCHO_PANTALLA / 2
        if len(centros) > 1 and max(centros) - min(centros) <= ANCHO_PANTALLA - MARGEN_CAMARA_CEMENTERIO * 2:
            minimo = max(centros) - ANCHO_PANTALLA + MARGEN_CAMARA_CEMENTERIO
            maximo = min(centros) - MARGEN_CAMARA_CEMENTERIO
            objetivo = min(max(objetivo, minimo), maximo)
        objetivo = max(0.0, min(objetivo, LARGO_NIVEL_CEMENTERIO - ANCHO_PANTALLA))
        factor = min(1.0, VELOCIDAD_CAMARA_CEMENTERIO * delta)
        self.x += (objetivo - self.x) * factor


class FondoCementerio:
    """Capas pixeladas repetibles con paralaje para el recorrido nocturno."""

    ANCHO_CAPA = ANCHO_PANTALLA * 2

    def __init__(self) -> None:
        self.cielo = self._cargar_capa("fondos/cementerio/cielo.png", (ANCHO_PANTALLA, ALTO_PANTALLA), self._crear_cielo)
        self.distancia = self._cargar_capa("fondos/cementerio/fondo_medio.png", (self.ANCHO_CAPA, ALTO_PANTALLA), self._crear_distancia)
        self.suelo = self._cargar_capa("fondos/cementerio/suelo.png", (self.ANCHO_CAPA, ALTO_PANTALLA), self._crear_suelo)
        self.vineta = self._crear_vineta()
        self.grano = self._crear_grano()
        self.mascara_luz = self._crear_mascara_luz()
        self.nieblas = self._crear_nieblas()
        self.capa_oscura = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        self.capa_luces = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)

    @staticmethod
    def _cargar_capa(
        ruta: str,
        tamano: tuple[int, int],
        crear_placeholder,
    ) -> pygame.Surface:
        imagen = CARGADOR_ASSETS.imagen(ruta)
        if imagen is not None:
            return pygame.transform.scale(imagen, tamano)
        return crear_placeholder()

    def _crear_cielo(self) -> pygame.Surface:
        superficie = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
        superficie.fill(PALETA_CEMENTERIO["cielo"])
        azar = random.Random(410)
        for _ in range(180):
            posicion = (azar.randrange(ANCHO_PANTALLA), azar.randrange(24, 260))
            tono = azar.choice((PALETA_CEMENTERIO["estrellas"], PALETA_CEMENTERIO["crater"], PALETA_CEMENTERIO["fondo_piedra"]))
            pygame.draw.rect(superficie, tono, (*posicion, azar.choice((1, 2)), 1))
        pygame.draw.circle(superficie, PALETA_CEMENTERIO["luna_sombra"], (747, 116), 59)
        pygame.draw.circle(superficie, PALETA_CEMENTERIO["luna"], (747, 116), 42)
        pygame.draw.circle(superficie, PALETA_CEMENTERIO["crater"], (734, 101), 8)
        pygame.draw.rect(superficie, PALETA_CEMENTERIO["crater"], (756, 125, 15, 7))
        pygame.draw.rect(superficie, PALETA_CEMENTERIO["crater"], (727, 132, 6, 9))
        return superficie

    def _crear_distancia(self) -> pygame.Surface:
        superficie = pygame.Surface((self.ANCHO_CAPA, ALTO_PANTALLA), pygame.SRCALPHA)
        azar = random.Random(304)
        for indice in range(14):
            posicion_x = indice * 151 + azar.randrange(-28, 29)
            base_y = 350 + azar.randrange(-18, 13)
            ancho = azar.randrange(42, 80)
            alto = azar.randrange(66, 128)
            rectangulo = pygame.Rect(posicion_x, base_y - alto, ancho, alto)
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["fondo_lejano"], rectangulo.inflate(10, 0))
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["fondo_piedra"], rectangulo, 3)
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["nicho_fondo"], rectangulo.inflate(-9, -10))
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol_borde"], rectangulo.midtop, rectangulo.midbottom, 2)
        for indice in range(18):
            posicion_x = indice * 119 + azar.randrange(-30, 31)
            altura = azar.randrange(74, 144)
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol"], (posicion_x, 378), (posicion_x - 13, 378 - altura), 5)
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol"], (posicion_x - 9, 378 - altura // 2), (posicion_x + 21, 378 - altura // 2 - 12), 4)
            for rama in range(3):
                inicio_y = 378 - altura + rama * 20
                pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol"], (posicion_x - 13, inicio_y), (posicion_x - 34, inicio_y - 19), 3)

        for posicion_x in (520, 1100, 2160, 3330, 4520, 5900, 7040, 8250, 9360):
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["nicho"], (posicion_x, 286, 44, 96))
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["metal"], (posicion_x, 286, 44, 96), 3)
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["nicho_fondo"], (posicion_x + 8, 294, 28, 74))
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol_borde"], (posicion_x + 14, 286), (posicion_x + 14, 382), 2)
            pygame.draw.line(superficie, PALETA_CEMENTERIO["arbol_borde"], (posicion_x + 30, 286), (posicion_x + 30, 382), 2)

        for posicion_x in (780, 1880, 2810, 4170, 6790, 8610):
            pygame.draw.rect(superficie, PALETA_CEMENTERIO["piedra"], (posicion_x, 320, 28, 52))
            pygame.draw.line(superficie, PALETA_CEMENTERIO["grabado"], (posicion_x + 12, 330), (posicion_x + 12, 362), 2)
            pygame.draw.line(superficie, PALETA_CEMENTERIO["grabado"], (posicion_x + 6, 344), (posicion_x + 18, 344), 2)

        return superficie

    def _crear_suelo(self) -> pygame.Surface:
        superficie = pygame.Surface((self.ANCHO_CAPA, ALTO_PANTALLA), pygame.SRCALPHA)
        pygame.draw.rect(superficie, PALETA_CEMENTERIO["suelo"], (0, ALTURA_SUELO_CEMENTERIO, self.ANCHO_CAPA, ALTO_PANTALLA - ALTURA_SUELO_CEMENTERIO))
        pygame.draw.line(superficie, PALETA_CEMENTERIO["tierra"], (0, ALTURA_SUELO_CEMENTERIO), (self.ANCHO_CAPA, ALTURA_SUELO_CEMENTERIO), 3)
        azar = random.Random(1204)
        for _ in range(620):
            posicion_x = azar.randrange(self.ANCHO_CAPA)
            posicion_y = azar.randrange(ALTURA_SUELO_CEMENTERIO + 5, ALTO_PANTALLA)
            color = azar.choice((PALETA_CEMENTERIO["tierra"], PALETA_CEMENTERIO["suelo"], PALETA_CEMENTERIO["fondo_piedra"]))
            pygame.draw.rect(superficie, color, (posicion_x, posicion_y, azar.randrange(2, 10), azar.randrange(1, 4)))
        for posicion_x in range(0, self.ANCHO_CAPA, 180):
            pygame.draw.rect(superficie, (47, 53, 48), (posicion_x + 16, ALTURA_SUELO_CEMENTERIO + 14, 90, 6))
            pygame.draw.rect(superficie, (68, 58, 49), (posicion_x + 26, ALTURA_SUELO_CEMENTERIO + 18, 22, 4))
        return superficie

    @staticmethod
    def _crear_vineta() -> pygame.Surface:
        superficie = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        for coordenada_y in range(ALTO_PANTALLA):
            for coordenada_x in range(ANCHO_PANTALLA):
                distancia = max(
                    abs(coordenada_x - ANCHO_PANTALLA / 2) / (ANCHO_PANTALLA / 2),
                    abs(coordenada_y - ALTO_PANTALLA / 2) / (ALTO_PANTALLA / 2),
                )
                fuerza = max(0.0, (distancia - 0.48) / 0.52)
                alpha = round(112 * float(EFECTOS_CEMENTERIO["vineta_intensidad"]) * fuerza * fuerza)
                if alpha:
                    superficie.set_at((coordenada_x, coordenada_y), (2, 4, 5, alpha))
        return superficie

    @staticmethod
    def _crear_grano() -> list[pygame.Surface]:
        fotogramas = []
        for indice in range(4):
            superficie = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
            azar = random.Random(510 + indice)
            for _ in range(2200):
                punto = (azar.randrange(ANCHO_PANTALLA), azar.randrange(ALTO_PANTALLA))
                gris = azar.choice(PALETA_CEMENTERIO["grano"])
                alpha = round(azar.randrange(8, 20) * float(EFECTOS_CEMENTERIO["grano_intensidad"]) * 5)
                superficie.set_at(punto, (gris, gris, gris, alpha))
            fotogramas.append(superficie)
        return fotogramas

    @staticmethod
    def _crear_mascara_luz() -> pygame.Surface:
        radio = int(EFECTOS_CEMENTERIO["linterna_radio"])
        mascara = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
        intensidad = float(EFECTOS_CEMENTERIO["linterna_intensidad"])
        for radio_actual in range(radio, 0, -4):
            distancia = radio_actual / radio
            alpha = round(255 * intensidad * (1 - distancia) ** 1.7)
            color_luz = (*PALETA_CEMENTERIO["luz"], alpha)
            pygame.draw.circle(mascara, color_luz, (radio, radio), radio_actual)
        return mascara

    @staticmethod
    def _crear_nieblas() -> list[pygame.Surface]:
        capas = []
        for semilla in (81, 92):
            niebla = pygame.Surface((ANCHO_PANTALLA * 2, 125), pygame.SRCALPHA)
            azar = random.Random(semilla)
            for _ in range(90):
                x = azar.randrange(niebla.get_width())
                y = azar.randrange(12, 108)
                ancho = azar.randrange(24, 130)
                alto = azar.randrange(3, 13)
                alpha = azar.randrange(8, 29)
                pygame.draw.ellipse(niebla, (*PALETA_CEMENTERIO["niebla"], alpha), (x, y, ancho, alto))
            niebla.set_alpha(int(EFECTOS_CEMENTERIO["niebla_alpha"]))
            capas.append(niebla)
        return capas

    def dibujar(self, pantalla: pygame.Surface, camara_x: float) -> None:
        pantalla.blit(self.cielo, (0, 0))
        desplazamiento = int(camara_x * 0.28) % self.ANCHO_CAPA
        pantalla.blit(self.distancia, (-desplazamiento, 0))
        pantalla.blit(self.distancia, (self.ANCHO_CAPA - desplazamiento, 0))
        desplazamiento_suelo = int(camara_x * 0.92) % self.ANCHO_CAPA
        pantalla.blit(self.suelo, (-desplazamiento_suelo, 0))
        pantalla.blit(self.suelo, (self.ANCHO_CAPA - desplazamiento_suelo, 0))

    def dibujar_efectos(
        self,
        pantalla: pygame.Surface,
        jugadores: list[JugadorCementerio],
        camara_x: float,
        tiempo: float,
    ) -> None:
        if EFECTOS_CEMENTERIO["niebla_habilitada"]:
            velocidades = (
                float(EFECTOS_CEMENTERIO["niebla_velocidad_lejana"]),
                float(EFECTOS_CEMENTERIO["niebla_velocidad_cercana"]),
            )
            posiciones_y = (294, 346)
            for indice, niebla in enumerate(self.nieblas):
                desplazamiento = int(tiempo * velocidades[indice]) % niebla.get_width()
                pantalla.blit(niebla, (-desplazamiento, posiciones_y[indice]))
                pantalla.blit(niebla, (niebla.get_width() - desplazamiento, posiciones_y[indice]))

        if EFECTOS_CEMENTERIO["iluminacion_habilitada"]:
            oscuridad = int(EFECTOS_CEMENTERIO["oscuridad_alpha"])
            if EFECTOS_CEMENTERIO["parpadeo_habilitado"]:
                amplitud = float(EFECTOS_CEMENTERIO["parpadeo_intensidad"])
                frecuencia = float(EFECTOS_CEMENTERIO["parpadeo_frecuencia"])
                oscuridad = round(oscuridad / (1 + amplitud * math.sin(tiempo * frecuencia * math.tau)))
            self.capa_oscura.fill((*PALETA_CEMENTERIO["noche"], oscuridad))
            self.capa_luces.fill((0, 0, 0, 0))
            if EFECTOS_CEMENTERIO["linterna_habilitada"]:
                for jugador in jugadores:
                    if jugador.estado in ("cayendo", "caido"):
                        continue
                    centro_x = round(jugador.rect.centerx - camara_x)
                    centro_y = jugador.rect.centery
                    radio = int(EFECTOS_CEMENTERIO["linterna_radio"])
                    self.capa_luces.blit(self.mascara_luz, (centro_x - radio, centro_y - radio))
            self.capa_oscura.blit(self.capa_luces, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            pantalla.blit(self.capa_oscura, (0, 0))

        if EFECTOS_CEMENTERIO["vineta_habilitada"]:
            pantalla.blit(self.vineta, (0, 0))
        if EFECTOS_CEMENTERIO["grano_habilitado"]:
            frecuencia_grano = max(1.0, float(EFECTOS_CEMENTERIO["grano_fps"]))
            indice_grano = int(tiempo * frecuencia_grano) % len(self.grano)
            pantalla.blit(self.grano[indice_grano], (0, 0))


class EscenaCementerio(BaseScene):
    """Primera versión: presentación, grupo de serenos y cámara lateral."""

    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        cantidad = 2 if estado_juego.cantidad_jugadores == 2 else 1
        esquemas = ("wasd", "flechas") if cantidad == 2 else ("ambos",)
        self.jugadores = [
            JugadorCementerio(indice, 120.0 + indice * 54, esquemas[indice])
            for indice in range(cantidad)
        ]
        ruta_nivel = Path(__file__).resolve().parents[2] / "data" / "nivel_cementerio.json"
        self.datos_nivel = json.loads(ruta_nivel.read_text(encoding="utf-8"))
        self.datos_nivel["tumba_final_x"] = (
            LARGO_NIVEL_CEMENTERIO - int(self.datos_nivel["separacion_meta_borde"])
        )
        self.obstaculos_datos = self.datos_nivel["obstaculos"]
        self.obstaculos_solidos = [
            pygame.Rect(
                int(obstaculo["x"]),
                ALTURA_SUELO_CEMENTERIO - int(obstaculo["alto"]),
                int(obstaculo["ancho"]),
                int(obstaculo["alto"]),
            )
            for obstaculo in self.obstaculos_datos
            if obstaculo["tipo"] in ("lapida", "nicho")
        ]
        self.camara = CamaraCementerio()
        self.fondo = FondoCementerio()
        self.dialogo: DialogueBox | None = DialogueBox(
            [{"speaker": " ", "text": self.textos["ui"]["cemetery_intro"]}]
        )
        self.fuente_dialogo = cargar_fuente(28)
        self.fase = "introduccion"
        self.opacidad = 0
        self.tiempo_fade = 0.0
        self.tiempo_escena = 0.0
        self.tiempo_final = 0.0
        self.tiempo_pasos = 0.0
        self.mostrar_colisiones = False
        self.game_over = False
        self.victima_rescate: int | None = None
        self.tiempo_rescate = 0.0
        self.toques_rescate = 0
        self.audio = AudioAmbiente(
            (
                "viento_cementerio",
                "grillos",
                "pasos_tierra",
                "salto",
                "caida_tumba",
                "rescate",
            )
        )
        self.audio.reproducir_ambientes(["viento_cementerio", "grillos"])
        self.pozos = [
            (int(obstaculo["x"]), int(obstaculo["x"]) + int(obstaculo["ancho"]))
            for obstaculo in self.obstaculos_datos
            if obstaculo["tipo"] == "pozo"
        ]
        if len(self.pozos) != CANTIDAD_TUMBAS_ABIERTAS_CEMENTERIO:
            print(
                "Advertencia: cantidad de tumbas abiertas del cementerio "
                f"= {len(self.pozos)}; se esperaba {CANTIDAD_TUMBAS_ABIERTAS_CEMENTERIO}."
            )
        self.tiempo_cartel = 0.0
        self.cartel_advertencia = self.textos["ui"]["cemetery_warning"]
        self.siluetas_finales = {
            "cantidad": int(SILUETAS_FINALES_CEMENTERIO["cantidad"]),
            "ancho": int(SILUETAS_FINALES_CEMENTERIO["ancho"]),
            "alto": int(SILUETAS_FINALES_CEMENTERIO["alto"]),
            "amplitud": float(SILUETAS_FINALES_CEMENTERIO["amplitud"]),
            "velocidad": float(SILUETAS_FINALES_CEMENTERIO["velocidad"]),
            "desfase": float(SILUETAS_FINALES_CEMENTERIO["desfase"]),
        }

    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F1:
            self.mostrar_colisiones = not self.mostrar_colisiones
            return
        if self.game_over:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                from juego.scenes.placeholder import Escena2Pendiente

                self.gestor.change_scene(Escena2Pendiente)
            return
        if self.fase == "introduccion" and self.dialogo is not None:
            if self.dialogo.avanzar(evento):
                self.dialogo = None
                self.fase = "fundido_a_negro"
                self.tiempo_fade = 0.0
            return
        if self.fase != "jugando" or evento.type != pygame.KEYDOWN:
            return
        if self.victima_rescate is not None and self._procesar_toque_rescate(evento.key):
            return
        for jugador in self.jugadores:
            teclas_salto = (pygame.K_w, pygame.K_UP) if jugador.esquema_controles == "ambos" else (
                (pygame.K_w,) if jugador.esquema_controles == "wasd" else (pygame.K_UP,)
            )
            if evento.key in teclas_salto:
                if jugador.saltar():
                    self.audio.reproducir_sfx("salto")

    def update(self, delta: float) -> None:
        self.tiempo_escena += delta
        if self.game_over:
            return
        if self.dialogo is not None:
            self.dialogo.update(delta)
        if self.fase == "jugando":
            self.tiempo_cartel += delta
        if self.fase in ("fundido_a_negro", "fundido_desde_negro"):
            self.tiempo_fade += delta
            progreso = min(1.0, self.tiempo_fade / SEGUNDOS_FADE_INTRO_CEMENTERIO)
            if self.fase == "fundido_a_negro":
                self.opacidad = round(255 * progreso)
                if progreso >= 1.0:
                    self.fase = "fundido_desde_negro"
                    self.tiempo_fade = 0.0
            else:
                self.opacidad = round(255 * (1.0 - progreso))
                if progreso >= 1.0:
                    self.fase = "jugando"
        elif self.fase == "final":
            self.tiempo_final += delta
            if self.tiempo_final >= SEGUNDOS_FINAL_CEMENTERIO:
                self.fase = "fundido_final"
                self.tiempo_fade = 0.0
        elif self.fase == "fundido_final":
            self.tiempo_fade += delta
            progreso = min(1.0, self.tiempo_fade / SEGUNDOS_FADE_INTRO_CEMENTERIO)
            self.opacidad = round(255 * progreso)
            if progreso >= 1.0:
                from juego.scenes.cinematica_2 import Cinematica2

                self.audio.detener_ambientes()
                self.gestor.change_scene(Cinematica2)
        if self.fase == "jugando":
            for indice, jugador in enumerate(self.jugadores):
                otro = self.jugadores[1 - indice] if len(self.jugadores) == 2 else None
                distancia_maxima = ANCHO_PANTALLA - MARGEN_CAMARA_CEMENTERIO * 2
                limites = (0.0, float(LARGO_NIVEL_CEMENTERIO - jugador.rect.width))
                if otro is not None:
                    limites = (
                        max(0.0, otro.rect.x - distancia_maxima),
                        min(float(LARGO_NIVEL_CEMENTERIO - jugador.rect.width), otro.rect.x + distancia_maxima),
                    )
                estado_anterior = jugador.estado
                jugador.update(delta, self.obstaculos_solidos, limites, self.pozos)
                if estado_anterior != "cayendo" and jugador.estado == "cayendo":
                    self.audio.reproducir_sfx("caida_tumba")
            self._actualizar_rescate(delta)
            self._actualizar_audio_pasos(delta)
            if not self.game_over and all(
                jugador.rect.centerx >= int(self.datos_nivel["tumba_final_x"])
                for jugador in self.jugadores
            ):
                self.fase = "final"
                self.tiempo_final = 0.0
        self.camara.actualizar(self.jugadores, delta)

    def draw(self, pantalla: pygame.Surface) -> None:
        for capa in CAPAS_CEMENTERIO:
            if capa == "fondo":
                self.fondo.dibujar(pantalla, self.camara.x)
            elif capa == "obstaculos":
                self._dibujar_obstaculos(pantalla)
            elif capa == "sombras":
                self._dibujar_sombras(pantalla)
            elif capa == "personajes":
                self._dibujar_personajes(pantalla)
            elif capa == "iluminacion_efectos":
                self.fondo.dibujar_efectos(pantalla, self.jugadores, self.camara.x, self.tiempo_escena)
            elif capa == "interfaz":
                self._dibujar_interfaz(pantalla)
                self._dibujar_cartel_advertencia(pantalla)
            elif capa == "fade":
                self._dibujar_fade(pantalla)

    def _dibujar_sombras(self, pantalla: pygame.Surface) -> None:
        if not EFECTOS_CEMENTERIO["sombras_habilitadas"] or self.fase == "final":
            return
        for jugador in self.jugadores:
            if jugador.estado in ("cayendo", "caido"):
                continue
            posicion_x = round(jugador.rect.centerx - self.camara.x)
            sombra = pygame.Rect(posicion_x - 19, ALTURA_SUELO_CEMENTERIO - 6, 38, 8)
            pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["sombra"], sombra)

    def _dibujar_personajes(self, pantalla: pygame.Surface) -> None:
        if self.fase == "final":
            self._dibujar_cuerpos_tumba_final(pantalla)
            return
        for jugador in self.jugadores:
            jugador.dibujar(pantalla, self.camara.x)

    def _dibujar_interfaz(self, pantalla: pygame.Surface) -> None:
        if self.dialogo is not None:
            self.dialogo.dibujar(
                pantalla,
                self.fuente_dialogo,
                self.textos["ui"]["dialogue_continue"],
            )
        if self.mostrar_colisiones:
            for inicio, fin in self.pozos:
                pygame.draw.rect(
                    pantalla,
                    PALETA_CEMENTERIO["debug_pozo"],
                    (round(inicio - self.camara.x), ALTURA_SUELO_CEMENTERIO - 4, fin - inicio, 18),
                    2,
                )
            for obstaculo in self.obstaculos_solidos:
                pantalla_rect = obstaculo.move(-round(self.camara.x), 0)
                pygame.draw.rect(pantalla, PALETA_CEMENTERIO["debug_colision"], pantalla_rect, 2)
            for jugador in self.jugadores:
                pygame.draw.rect(pantalla, PALETA_CEMENTERIO["debug_jugador"], jugador.rect.move(-round(self.camara.x), 0), 2)
            etiqueta = self.gestor.fuente.render("F1: colisiones", True, PALETA_CEMENTERIO["debug_texto"])
            pantalla.blit(etiqueta, (16, 16))
        if self.game_over:
            self._dibujar_game_over(pantalla)
        elif self.victima_rescate is not None:
            self._dibujar_indicador_rescate(pantalla)

    def _dibujar_fade(self, pantalla: pygame.Surface) -> None:
        if not self.opacidad:
            return
        capa_negra = pygame.Surface(pantalla.get_size())
        capa_negra.fill((0, 0, 0))
        capa_negra.set_alpha(self.opacidad)
        pantalla.blit(capa_negra, (0, 0))

    def _dibujar_obstaculos(self, pantalla: pygame.Surface) -> None:
        for obstaculo in self.obstaculos_datos:
            x = int(obstaculo["x"] - self.camara.x)
            ancho = int(obstaculo["ancho"])
            if obstaculo["tipo"] == "pozo":
                pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["pozo"], (x, ALTURA_SUELO_CEMENTERIO - 12, ancho, 28))
                pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["borde_pozo"], (x - 5, ALTURA_SUELO_CEMENTERIO - 13, ancho + 10, 8))
                pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["pozo_sombra"], (x + 5, ALTURA_SUELO_CEMENTERIO - 10, ancho - 10, 5))
                continue
            alto = int(obstaculo["alto"])
            rectangulo = pygame.Rect(x, ALTURA_SUELO_CEMENTERIO - alto, ancho, alto)
            if EFECTOS_CEMENTERIO["sombras_habilitadas"]:
                pygame.draw.ellipse(pantalla, (17, 19, 17), (x - 8, ALTURA_SUELO_CEMENTERIO - 5, ancho + 16, 9))
            if obstaculo["tipo"] == "lapida":
                cuerpo = pygame.Rect(x, rectangulo.y + 8, ancho, alto - 8)
                pygame.draw.rect(pantalla, PALETA_CEMENTERIO["piedra"], cuerpo)
                pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["piedra"], (x, rectangulo.y, ancho, 18))
                pygame.draw.line(pantalla, PALETA_CEMENTERIO["piedra_luz"], (x + 6, rectangulo.y + 10), (x + 6, rectangulo.bottom - 5), 2)
                pygame.draw.line(pantalla, (27, 33, 31), (x + ancho - 4, rectangulo.y + 14), (x + ancho - 4, rectangulo.bottom), 3)
                pygame.draw.line(pantalla, PALETA_CEMENTERIO["grabado"], (x + ancho // 2, rectangulo.y + 23), (x + ancho // 2, rectangulo.y + alto // 2), 2)
                pygame.draw.line(pantalla, PALETA_CEMENTERIO["grabado"], (x + ancho // 2 - 7, rectangulo.y + 31), (x + ancho // 2 + 7, rectangulo.y + 31), 2)
            else:
                pygame.draw.rect(pantalla, PALETA_CEMENTERIO["nicho"], rectangulo)
                pygame.draw.rect(pantalla, PALETA_CEMENTERIO["metal"], rectangulo, 4)
                for linea_y in range(rectangulo.y + 17, rectangulo.bottom - 5, 19):
                    pygame.draw.line(pantalla, PALETA_CEMENTERIO["fondo_piedra"], (x + 5, linea_y), (x + ancho - 5, linea_y), 2)
                pygame.draw.rect(pantalla, (18, 24, 24), (x + ancho // 2 - 2, rectangulo.y + 9, 4, alto - 18))

        tumba_x = round(int(self.datos_nivel["tumba_final_x"]) - self.camara.x)
        lapida_final = pygame.Rect(tumba_x + 65, ALTURA_SUELO_CEMENTERIO - 142, 52, 118)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["lapida_final"], lapida_final)
        pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["lapida_final"], (lapida_final.x, lapida_final.y - 20, lapida_final.w, 40))
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["grabado"], lapida_final, 3)
        pygame.draw.line(pantalla, PALETA_CEMENTERIO["lapida_final_linea"], (lapida_final.centerx, lapida_final.y + 18), (lapida_final.centerx, lapida_final.y + 78), 4)
        pygame.draw.line(pantalla, PALETA_CEMENTERIO["lapida_final_linea"], (lapida_final.x + 12, lapida_final.y + 39), (lapida_final.right - 12, lapida_final.y + 39), 4)
        plataforma = pygame.Rect(tumba_x, ALTURA_SUELO_CEMENTERIO - 20, 184, 22)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["plataforma_final"], plataforma)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["plataforma_borde"], plataforma, 3)
        pygame.draw.ellipse(pantalla, PALETA_CEMENTERIO["sombra"], (tumba_x - 12, ALTURA_SUELO_CEMENTERIO - 3, 210, 15))

    def _dibujar_cuerpos_tumba_final(self, pantalla: pygame.Surface) -> None:
        tumba_x = round(int(self.datos_nivel["tumba_final_x"]) - self.camara.x)
        for indice in range(self.siluetas_finales["cantidad"]):
            offset = math.sin(self.tiempo_final * self.siluetas_finales["velocidad"] + indice * self.siluetas_finales["desfase"]) * self.siluetas_finales["amplitud"]
            cuerpo_x = tumba_x + 26 + indice * 76
            cuerpo_y = ALTURA_SUELO_CEMENTERIO - 36 + offset
            silueta = pygame.Surface((self.siluetas_finales["ancho"], self.siluetas_finales["alto"]), pygame.SRCALPHA)
            pygame.draw.ellipse(silueta, (7, 9, 9, 180), (0, 0, self.siluetas_finales["ancho"], 18))
            pygame.draw.rect(silueta, (7, 9, 9, 180), (8, 14, 20, 20))
            pygame.draw.rect(silueta, (7, 9, 9, 180), (5, 32, 26, 18))
            pygame.draw.ellipse(silueta, (7, 9, 9, 180), (0, 20, 12, 16))
            pygame.draw.ellipse(silueta, (7, 9, 9, 180), (20, 20, 12, 16))
            pantalla.blit(silueta, (cuerpo_x, cuerpo_y))

        marcador = pygame.Rect(tumba_x + 70, ALTURA_SUELO_CEMENTERIO - 112, 40, 16)
        pygame.draw.rect(pantalla, (7, 9, 9), marcador)

    def _dibujar_cartel_advertencia(self, pantalla: pygame.Surface) -> None:
        if self.fase != "jugando":
            return
        if self.tiempo_cartel >= DURACION_CARTEL_ADVERTENCIA_CEMENTERIO * 2.0:
            return
        if self.tiempo_cartel < 0.2:
            fade = min(1.0, self.tiempo_cartel / 0.2)
        elif self.tiempo_cartel > DURACION_CARTEL_ADVERTENCIA_CEMENTERIO:
            fade = max(0.0, 1.0 - (self.tiempo_cartel - DURACION_CARTEL_ADVERTENCIA_CEMENTERIO) / 0.7)
        else:
            fade = 1.0
        alpha = max(0, min(255, int(255 * fade)))
        panel = pygame.Rect(170, 18, 620, 48)
        fondo = pygame.Surface(panel.size, pygame.SRCALPHA)
        fondo.fill((8, 11, 13, int(140 * fade)))
        pygame.draw.rect(fondo, (*PALETA_CEMENTERIO["panel_borde"], int(180 * fade)), panel, 2)
        texto = self.gestor.fuente.render(self.cartel_advertencia, True, (*PALETA_CEMENTERIO["texto"], alpha))
        pantalla.blit(fondo, panel.topleft)
        pantalla.blit(texto, (panel.centerx - texto.get_width() // 2, panel.y + 13))

    def _dibujar_game_over(self, pantalla: pygame.Surface) -> None:
        capa = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
        capa.fill((*PALETA_CEMENTERIO["gameover_velo"], 218))
        pantalla.blit(capa, (0, 0))
        titulo = self.gestor.fuente_grande.render(self.textos["ui"]["game_over"], True, PALETA_CEMENTERIO["gameover_titulo"])
        clave_razon = "cemetery_fall_reason" if len(self.jugadores) == 1 else "cemetery_fail_reason"
        razon = self.gestor.fuente.render(self.textos["ui"][clave_razon], True, PALETA_CEMENTERIO["gameover_texto"])
        reintento = cargar_fuente(20).render(self.textos["ui"]["retry"], True, PALETA_CEMENTERIO["gameover_ayuda"])
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO_PANTALLA // 2, 285)))
        pantalla.blit(razon, razon.get_rect(center=(ANCHO_PANTALLA // 2, 330)))
        pantalla.blit(reintento, reintento.get_rect(center=(ANCHO_PANTALLA // 2, 375)))

    def _procesar_toque_rescate(self, tecla: int) -> bool:
        if self.victima_rescate is None:
            return False
        victima = self.jugadores[self.victima_rescate]
        if victima.estado != "caido":
            return False
        indice_rescatista = 1 - self.victima_rescate
        rescatista = self.jugadores[indice_rescatista]
        if rescatista.estado != "normal" or not self._rescatista_cerca(rescatista, victima):
            return False
        teclas_validas = (pygame.K_f,) if rescatista.esquema_controles == "wasd" else (
            pygame.K_0,
            pygame.K_KP0,
        )
        if tecla not in teclas_validas:
            return False
        self.toques_rescate += 1
        if self.toques_rescate >= TOQUES_RESCATE_NECESARIOS:
            victima.iniciar_rescate()
            self.audio.reproducir_sfx("rescate")
        return True

    def _actualizar_audio_pasos(self, delta: float) -> None:
        caminando = any(jugador.moviendo and jugador.estado == "normal" for jugador in self.jugadores)
        if not caminando:
            self.tiempo_pasos = 0.0
            return
        self.tiempo_pasos += delta
        if self.tiempo_pasos >= INTERVALO_PASOS_CEMENTERIO:
            self.audio.reproducir_sfx("pasos_tierra")
            self.tiempo_pasos = 0.0

    def _perder(self) -> None:
        if not self.game_over:
            self.game_over = True
            self.audio.detener_ambientes()

    def _actualizar_rescate(self, delta: float) -> None:
        caidos = [
            indice
            for indice, jugador in enumerate(self.jugadores)
            if jugador.estado in ("cayendo", "caido")
        ]
        if len(caidos) >= 2:
            self._perder()
            return
        if self.victima_rescate is not None:
            indice_rescatista = 1 - self.victima_rescate
            if indice_rescatista in caidos:
                self._perder()
                return
            victima_actual = self.jugadores[self.victima_rescate]
            if victima_actual.estado == "normal":
                self.victima_rescate = None
                self.tiempo_rescate = 0.0
                self.toques_rescate = 0
                return
        if not caidos:
            return
        if len(self.jugadores) == 1:
            if caidos[0] == 0 and self.jugadores[0].estado == "caido":
                self._perder()
            return
        if self.victima_rescate is None:
            self.victima_rescate = caidos[0]
            self.tiempo_rescate = SEGUNDOS_RESCATE
            self.toques_rescate = 0
        victima = self.jugadores[self.victima_rescate]
        if victima.estado in ("cayendo", "caido"):
            self.tiempo_rescate = max(0.0, self.tiempo_rescate - delta)
            if self.tiempo_rescate == 0.0:
                self._perder()

    @staticmethod
    def _rescatista_cerca(rescatista: JugadorCementerio, victima: JugadorCementerio) -> bool:
        posicion_pozo = getattr(victima, "posicion_pozo", None)
        return posicion_pozo is not None and abs(rescatista.rect.centerx - posicion_pozo) <= DISTANCIA_RESCATE

    def _dibujar_indicador_rescate(self, pantalla: pygame.Surface) -> None:
        victima = self.jugadores[self.victima_rescate]
        posicion_pozo = getattr(victima, "posicion_pozo", victima.rect.centerx)
        centro_x = round(posicion_pozo - self.camara.x)
        cerca = self._rescatista_cerca(self.jugadores[1 - self.victima_rescate], victima)
        tecla = "F" if self.jugadores[1 - self.victima_rescate].esquema_controles == "wasd" else "0"
        color = PALETA_CEMENTERIO["indicador_activo"] if cerca else PALETA_CEMENTERIO["indicador_inactivo"]
        glifo = cargar_fuente(24).render(tecla, True, color)
        caja_glifo = pygame.Rect(centro_x - 17, ALTURA_SUELO_CEMENTERIO - 77, 34, 31)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["panel_ui"], caja_glifo)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["ui_desactivada"], caja_glifo, 2)
        pantalla.blit(glifo, glifo.get_rect(center=caja_glifo.center))

        panel = pygame.Rect(ANCHO_PANTALLA // 2 - 152, 20, 304, 58)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["panel_ui"], panel)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["panel_borde"], panel, 2)
        etiqueta = self.gestor.fuente.render(
            f"RESCATE  {self.tiempo_rescate:04.1f}s  {self.toques_rescate}/{TOQUES_RESCATE_NECESARIOS}",
            True,
            PALETA_CEMENTERIO["texto"],
        )
        pantalla.blit(etiqueta, etiqueta.get_rect(center=(panel.centerx, panel.y + 17)))
        barra = pygame.Rect(panel.x + 12, panel.y + 34, panel.w - 24, 11)
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["barra_fondo"], barra)
        ancho_progreso = round(barra.w * min(1.0, self.toques_rescate / TOQUES_RESCATE_NECESARIOS))
        if ancho_progreso:
            pygame.draw.rect(pantalla, PALETA_CEMENTERIO["acento"], (barra.x, barra.y, ancho_progreso, barra.h))
        pygame.draw.rect(pantalla, PALETA_CEMENTERIO["barra_borde"], barra, 1)