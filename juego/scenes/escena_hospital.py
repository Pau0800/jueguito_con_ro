"""Recepción y pasillo: primera escena jugable."""

import random

import pygame

from juego.config import (
    ALTO_PANTALLA,
    CANTIDAD_PUERTAS_SALA_1,
    CANTIDAD_PUERTAS_SALA_2,
    TIEMPO_BUSQUEDA_SEGUNDOS,
)
from juego import estado_juego
from juego.scenes.base_scene import BaseScene
from juego.scenes.cinematica import Cinematica1
from juego.systems.ambiente import AmbienteHospital
from juego.systems.audio_ambiente import AudioAmbiente
from juego.systems.fonts import cargar_fuente
from juego.systems.dialogue import DialogueBox
from juego.systems.input import jugador_que_acciona
from juego.systems.player import Periodista


ANCHO = 960


class EscenaHospital(BaseScene):
    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        self.zona = "recepcion"
        self.jugadores = [
            Periodista(0, (105, 300), "wasd" if estado_juego.cantidad_jugadores == 2 else "ambos")
        ]
        if estado_juego.cantidad_jugadores == 2:
            self.jugadores.append(Periodista(1, (150, 300), "flechas"))
        self.esperando_otro = False
        self.mostrar_colisiones = False
        self.tiempo_ambiente = 0.0
        self.ambiente = AmbienteHospital()
        self.audio = AudioAmbiente()
        self.dialogo: DialogueBox | None = None
        self.pasillo_desbloqueado = False
        self.tiempo_restante = float(TIEMPO_BUSQUEDA_SEGUNDOS)
        self.temporizador_activo = False
        self.game_over = False
        self.mensaje_puerta = ""
        self.tiempo_mensaje = 0.0
        self.transicion_programada = False
        self.puertas = self._crear_puertas()
        self.puerta_correcta = self._elegir_puerta_correcta()
        self.fuentes = {
            "cartel": cargar_fuente(26),
            "pequena": cargar_fuente(20),
        }

    def _elegir_puerta_correcta(self) -> int:
        return random.choice([int(puerta["id"]) for puerta in self.puertas])

    @staticmethod
    def _crear_puertas() -> list[dict[str, object]]:
        puertas = []
        distribucion = (
            ("sala1", ((170, 106, "arriba"), (390, 106, "arriba"), (610, 386, "abajo"), (810, 386, "abajo"))),
            ("sala2", ((170, 106, "arriba"), (390, 106, "arriba"), (610, 386, "abajo"))),
        )
        identificador = 1
        for sala, posiciones in distribucion:
            cantidad_esperada = CANTIDAD_PUERTAS_SALA_1 if sala == "sala1" else CANTIDAD_PUERTAS_SALA_2
            for x, y, lado in posiciones[:cantidad_esperada]:
                puertas.append(
                    {"id": identificador, "sala": sala, "x": x, "y": y, "lado": lado}
                )
                identificador += 1
        return puertas

    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F1:
            self.mostrar_colisiones = not self.mostrar_colisiones
            return
        if self.game_over:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                self.gestor.change_scene(EscenaHospital)
            return

        if self.dialogo is not None:
            if self.dialogo.avanzar(evento):
                self.dialogo = None
                self.pasillo_desbloqueado = True
                self.temporizador_activo = True
            return

        indice_jugador = jugador_que_acciona(evento)
        if indice_jugador is None or indice_jugador >= len(self.jugadores):
            return

        jugador = self.jugadores[indice_jugador]
        if self.zona == "recepcion" and self._cerca_de_recepcionista(jugador):
            self.dialogo = DialogueBox(self.textos["dialogues"]["receptionist"])
        elif self.zona in ("sala1", "sala2"):
            puerta = self._puerta_cercana(jugador)
            if puerta is not None:
                self._revisar_puerta(int(puerta["id"]))

    def update(self, delta: float) -> None:
        self.tiempo_ambiente += delta
        if self.game_over:
            return

        if self.temporizador_activo:
            self.tiempo_restante -= delta
            if self.tiempo_restante <= 0:
                self.tiempo_restante = 0
                self.game_over = True
                return

        if self.tiempo_mensaje > 0:
            self.tiempo_mensaje = max(0, self.tiempo_mensaje - delta)
            if self.tiempo_mensaje == 0:
                if self.transicion_programada:
                    self.gestor.change_scene(Cinematica1)
                    self.transicion_programada = False
                else:
                    self.mensaje_puerta = ""

        if self.dialogo is not None:
            self.dialogo.update(delta)
            return
        if self.mensaje_puerta == self.textos["ui"]["correct_door"]:
            return

        obstaculos = self._obstaculos_actuales()
        for jugador in self.jugadores:
            jugador.update(delta, obstaculos)
        self._comprobar_transicion_sala()
        self.audio.actualizar(delta, any(jugador.moviendo for jugador in self.jugadores))

    def _obstaculos_actuales(self) -> list[pygame.Rect]:
        if self.zona == "recepcion":
            obstaculos = [
                pygame.Rect(0, 0, ANCHO, 155),
                pygame.Rect(0, ALTO_PANTALLA - 22, ANCHO, 22),
                pygame.Rect(0, 0, 22, ALTO_PANTALLA),
                pygame.Rect(ANCHO - 22, 0, 22, 210),
                pygame.Rect(ANCHO - 22, 352, 22, ALTO_PANTALLA - 352),
                pygame.Rect(260, 112, 440, 141),
            ]
            if not self.pasillo_desbloqueado:
                obstaculos.append(pygame.Rect(ANCHO - 22, 210, 22, 142))
            return obstaculos

        obstaculos = [
            pygame.Rect(0, 0, ANCHO, 92),
            pygame.Rect(0, 462, ANCHO, 78),
            pygame.Rect(0, 0, 22, 210),
            pygame.Rect(0, 352, 22, ALTO_PANTALLA - 352),
            pygame.Rect(ANCHO - 22, 0, 22, 210),
            pygame.Rect(ANCHO - 22, 352, 22, ALTO_PANTALLA - 352),
        ]
        for puerta in self.puertas:
            if puerta["sala"] != self.zona:
                continue
            x = int(puerta["x"])
            if puerta["lado"] == "arriba":
                obstaculos.append(pygame.Rect(x - 40, 92, 80, 45))
            else:
                obstaculos.append(pygame.Rect(x - 40, 415, 80, 47))
        return obstaculos

    def _salida_actual(self) -> tuple[str, str] | None:
        if self.zona == "recepcion":
            return ("derecha", "sala1") if self.pasillo_desbloqueado else None
        if self.zona == "sala1":
            return "izquierda", "recepcion"
        if self.zona == "sala2":
            return "izquierda", "sala1"
        return None

    def _comprobar_transicion_sala(self) -> None:
        salida = self._salida_actual()
        if salida is None:
            self.esperando_otro = False
            return
        lado, destino = salida
        if self.zona == "sala1" and any(
            self._esta_en_salida(jugador, "derecha") for jugador in self.jugadores
        ):
            lado, destino = "derecha", "sala2"

        en_zona = [self._esta_en_salida(jugador, lado) for jugador in self.jugadores]
        self.esperando_otro = len(self.jugadores) == 2 and any(en_zona) and not all(en_zona)
        if all(en_zona):
            self.zona = destino
            for indice, jugador in enumerate(self.jugadores):
                if lado == "derecha":
                    jugador.rect.topleft = (70 + indice * 40, 250)
                else:
                    jugador.rect.topleft = (ANCHO - 110 - indice * 40, 250)
            self.esperando_otro = False
            return

        if self.esperando_otro:
            for jugador, dentro in zip(self.jugadores, en_zona):
                if dentro and lado == "derecha":
                    jugador.rect.right = ANCHO - 22
                elif dentro and lado == "izquierda":
                    jugador.rect.left = 22

    @staticmethod
    def _esta_en_salida(jugador: Periodista, lado: str) -> bool:
        rect = jugador.rect
        if rect.top < 210 or rect.bottom > 352:
            return False
        if lado == "derecha":
            return rect.centerx >= ANCHO - 55
        return rect.centerx <= 55

    @staticmethod
    def _cerca_de_recepcionista(jugador: Periodista) -> bool:
        rect = jugador.rect
        return 280 <= rect.centerx <= 680 and 245 <= rect.bottom <= 345

    def _puerta_cercana(self, jugador: Periodista) -> dict[str, object] | None:
        centro_jugador = pygame.Vector2(jugador.rect.center)
        for puerta in self.puertas:
            if puerta["sala"] != self.zona:
                continue
            centro_puerta = pygame.Vector2(int(puerta["x"]), int(puerta["y"]))
            if centro_jugador.distance_to(centro_puerta) < 76:
                return puerta
        return None

    def _revisar_puerta(self, identificador: int) -> None:
        if identificador == self.puerta_correcta:
            self.mensaje_puerta = self.textos["ui"]["correct_door"]
            self.tiempo_mensaje = 1.2
            self.transicion_programada = True
            self.temporizador_activo = False
        else:
            self.mensaje_puerta = self.textos["ui"]["wrong_door"]
            self.tiempo_mensaje = 1.5

    def draw(self, pantalla: pygame.Surface) -> None:
        self.ambiente.dibujar_fondo(pantalla, self.zona, self.tiempo_ambiente)
        nombre_zona = "reception_sign" if self.zona == "recepcion" else (
            "room_one_sign" if self.zona == "sala1" else "room_two_sign"
        )
        self._etiqueta(pantalla, self.textos["ui"][nombre_zona], (ANCHO // 2, 23))

        for jugador in self.jugadores:
            jugador.dibujar(pantalla)
        self.ambiente.aplicar_atmosfera(
            pantalla,
            [jugador.rect for jugador in self.jugadores],
            self.tiempo_ambiente,
        )
        if self.temporizador_activo:
            self._dibujar_temporizador(pantalla)
        self._dibujar_indicacion(pantalla)
        if self.esperando_otro:
            self._etiqueta(
                pantalla,
                self.textos["ui"]["waiting_player"],
                (ANCHO // 2, ALTO_PANTALLA - 70),
            )

        if self.mensaje_puerta and self.tiempo_mensaje > 0:
            self._dibujar_cartel_central(pantalla, self.mensaje_puerta)
        if self.dialogo is not None:
            ayuda_dialogo = "dialogue_continue_two_players" if len(self.jugadores) == 2 else "dialogue_continue"
            self.dialogo.dibujar(
                pantalla,
                self.gestor.fuente,
                self.textos["ui"][ayuda_dialogo],
            )
        if self.game_over:
            self._dibujar_game_over(pantalla)
        if self.mostrar_colisiones:
            self._dibujar_colisiones(pantalla)

    def _dibujar_recepcion(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((31, 34, 34))
        for y in range(26, ALTO_PANTALLA - 20, 42):
            pygame.draw.line(pantalla, (40, 43, 42), (24, y), (ANCHO - 24, y), 1)
        pygame.draw.rect(pantalla, (51, 55, 53), (22, 22, ANCHO - 44, 54))
        pygame.draw.rect(pantalla, (80, 84, 78), (370, 52, 220, 6))
        pygame.draw.rect(pantalla, (91, 85, 70), (270, 175, 420, 78))
        pygame.draw.rect(pantalla, (119, 108, 87), (260, 162, 440, 20))
        pygame.draw.rect(pantalla, (64, 66, 62), (288, 190, 12, 61))
        pygame.draw.rect(pantalla, (64, 66, 62), (660, 190, 12, 61))
        self._dibujar_persona_estatica(pantalla, 464, 112, (76, 87, 81))
        self._etiqueta(pantalla, self.textos["ui"]["reception_sign"], (480, 96))
        pygame.draw.rect(pantalla, (90, 84, 68), (ANCHO - 32, 216, 10, 114))
        pygame.draw.rect(pantalla, (53, 56, 54), (35, 90, 150, 52))
        pygame.draw.rect(pantalla, (91, 88, 76), (45, 101, 130, 3))

    def _dibujar_pasillo(self, pantalla: pygame.Surface) -> None:
        pantalla.fill((25, 28, 29))
        pygame.draw.rect(pantalla, (43, 46, 45), (0, 92, ANCHO, 370))
        for x in range(22, ANCHO, 72):
            pygame.draw.line(pantalla, (48, 51, 50), (x, 112), (x, 447), 1)
        pygame.draw.rect(pantalla, (51, 54, 52), (0, 0, ANCHO, 92))
        pygame.draw.rect(pantalla, (51, 54, 52), (0, 462, ANCHO, 78))
        for puerta in self.puertas:
            if puerta["sala"] != self.zona:
                continue
            x = int(puerta["x"])
            if puerta["lado"] == "arriba":
                rect = pygame.Rect(x - 35, 68, 70, 54)
            else:
                rect = pygame.Rect(x - 35, 438, 70, 48)
            pygame.draw.rect(pantalla, (65, 61, 54), rect)
            pygame.draw.rect(pantalla, (103, 94, 75), rect, 2)
            pygame.draw.rect(pantalla, (46, 47, 44), (rect.x + 8, rect.y + 7, rect.w - 16, rect.h - 14))
            pygame.draw.circle(pantalla, (155, 136, 94), (rect.right - 12, rect.centery), 3)
        pygame.draw.rect(pantalla, (78, 77, 67), (0, 216, 14, 114))
        pygame.draw.rect(pantalla, (78, 77, 67), (ANCHO - 14, 216, 14, 114))
        nombre_sala = "room_one_sign" if self.zona == "sala1" else "room_two_sign"
        self._etiqueta(pantalla, self.textos["ui"][nombre_sala], (ANCHO // 2, 38))

    def _dibujar_temporizador(self, pantalla: pygame.Surface) -> None:
        segundos = max(0, int(self.tiempo_restante + 0.999))
        texto = self.textos["ui"]["timer"].format(seconds=f"00:{segundos:02d}")
        imagen = self.gestor.fuente.render(texto, True, (223, 211, 181))
        fondo = pygame.Rect(ANCHO - imagen.get_width() - 34, 15, imagen.get_width() + 20, 38)
        pygame.draw.rect(pantalla, (17, 19, 19), fondo)
        pantalla.blit(imagen, (fondo.x + 10, fondo.y + 7))

    def _dibujar_indicacion(self, pantalla: pygame.Surface) -> None:
        if self.game_over or self.dialogo is not None or self.mensaje_puerta:
            return
        texto = None
        if self.zona == "recepcion" and not self.pasillo_desbloqueado and any(
            self._cerca_de_recepcionista(jugador) for jugador in self.jugadores
        ):
            clave = "receptionist_prompt_two_players" if len(self.jugadores) == 2 else "receptionist_prompt"
            texto = self.textos["ui"][clave]
        elif self.zona in ("sala1", "sala2") and any(
            self._puerta_cercana(jugador) is not None for jugador in self.jugadores
        ):
            clave = "door_prompt_two_players" if len(self.jugadores) == 2 else "door_prompt"
            texto = self.textos["ui"][clave]
        if texto:
            self._etiqueta(pantalla, texto, (ANCHO // 2, ALTO_PANTALLA - 36))
        elif self.zona == "recepcion" and not self.pasillo_desbloqueado:
            self._etiqueta(pantalla, self.textos["ui"]["locked_prompt"], (ANCHO // 2, ALTO_PANTALLA - 36))

    def _dibujar_cartel_central(self, pantalla: pygame.Surface, texto: str) -> None:
        caja = pygame.Rect(260, 222, 440, 76)
        pygame.draw.rect(pantalla, (13, 15, 16), caja)
        pygame.draw.rect(pantalla, (131, 119, 95), caja, 2)
        imagen = self.gestor.fuente_grande.render(texto, True, (227, 219, 199))
        pantalla.blit(imagen, imagen.get_rect(center=caja.center))

    def _dibujar_game_over(self, pantalla: pygame.Surface) -> None:
        capa = pygame.Surface((ANCHO, ALTO_PANTALLA), pygame.SRCALPHA)
        capa.fill((5, 7, 9, 205))
        pantalla.blit(capa, (0, 0))
        self._dibujar_persona_estatica(pantalla, 468, 178, (90, 91, 86))
        titulo = self.gestor.fuente_grande.render(self.textos["ui"]["game_over"], True, (208, 199, 183))
        razon = self.gestor.fuente.render(self.textos["ui"]["game_over_reason"], True, (184, 180, 169))
        reintento = self.fuentes["pequena"].render(self.textos["ui"]["retry"], True, (151, 156, 150))
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 300)))
        pantalla.blit(razon, razon.get_rect(center=(ANCHO // 2, 343)))
        pantalla.blit(reintento, reintento.get_rect(center=(ANCHO // 2, 385)))

    def _dibujar_colisiones(self, pantalla: pygame.Surface) -> None:
        for obstaculo in self._obstaculos_actuales():
            pygame.draw.rect(pantalla, (220, 35, 45), obstaculo, 2)
        for jugador in self.jugadores:
            pygame.draw.rect(pantalla, (55, 235, 120), jugador.rect, 2)
        etiqueta = self.fuentes["pequena"].render("F1: colisiones", True, (240, 220, 190))
        pantalla.blit(etiqueta, (16, 16))

    def _etiqueta(self, pantalla: pygame.Surface, texto: str, centro: tuple[int, int]) -> None:
        imagen = self.fuentes["cartel"].render(texto, True, (210, 204, 185))
        pantalla.blit(imagen, imagen.get_rect(center=centro))

    @staticmethod
    def _dibujar_persona_estatica(
        pantalla: pygame.Surface, x: int, y: int, color_ropa: tuple[int, int, int]
    ) -> None:
        pygame.draw.rect(pantalla, (166, 146, 123), (x + 8, y, 17, 16))
        pygame.draw.rect(pantalla, color_ropa, (x + 4, y + 16, 25, 28))
        pygame.draw.rect(pantalla, (40, 41, 40), (x + 5, y + 44, 9, 12))
        pygame.draw.rect(pantalla, (40, 41, 40), (x + 20, y + 44, 9, 12))