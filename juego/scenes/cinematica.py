"""Escena reutilizable que reproduce una cinemática declarada en JSON."""

import pygame

from juego import estado_juego
from juego.config import (
    ALTO_PANTALLA,
    ANCHO_PANTALLA,
    DURACION_ESPERA_CINEMATICA,
    DURACION_FADE_CINEMATICA,
    FPS_ANIMACION_PERSONAJE,
    SALTAR_CINEMATICA_HABILITADO,
    TAMANO_CELDA_PERSONAJE,
    TECLA_SALTAR_CINEMATICA,
)
from juego.scenes.base_scene import BaseScene
from juego.scenes.placeholder import Escena2Pendiente
from juego.systems.cutscene import CinematicPlayer
from juego.systems.dialogue import DialogueBox
from juego.systems.fonts import cargar_fuente
from juego.systems.animation import SpriteAnimado
from juego.systems.assets import CARGADOR_ASSETS
from juego.systems.audio_ambiente import AudioManager
from juego.systems.cinematic_room import CinematicRoomRenderer


class CinematicScene(BaseScene):
    """Presenta actores y eventos de una cinemática a partir de datos."""

    def __init__(self, gestor, id_cinematica: str, id_habitacion: str) -> None:
        super().__init__(gestor)
        datos = self.textos["cinematics"]
        self.id_cinematica = id_cinematica
        self.habitacion = datos["rooms"][id_habitacion]
        self.actores = {
            actor["id"]: {**actor, "visible": False}
            for actor in self.habitacion["characters"]
        }
        self.eventos = datos[id_cinematica]
        self.reproductor = CinematicPlayer(
            self.eventos,
            {
                "DURACION_FADE_CINEMATICA": DURACION_FADE_CINEMATICA,
                "DURACION_ESPERA_CINEMATICA": DURACION_ESPERA_CINEMATICA,
            },
        )
        self.dialogo: DialogueBox | None = None
        self.fuente_dialogo = cargar_fuente(28)
        self.habitacion_renderer = CinematicRoomRenderer(self.habitacion)
        self.animaciones = {
            actor["id"]: SpriteAnimado(
                2 + indice if actor["kind"] == "chica" else indice,
                str(actor["sprite"]),
                TAMANO_CELDA_PERSONAJE,
                FPS_ANIMACION_PERSONAJE,
            )
            for indice, actor in enumerate(self.habitacion["characters"])
        }
        self.audio = AudioManager()
        self.tiempo_escena = 0.0

    def handle_event(self, evento: pygame.event.Event) -> None:
        if (
            SALTAR_CINEMATICA_HABILITADO
            and evento.type == pygame.KEYDOWN
            and evento.key == pygame.key.key_code(TECLA_SALTAR_CINEMATICA)
        ):
            self.audio.detener_ambientes()
            self.gestor.change_scene(Escena2Pendiente)
            return

        if self.dialogo is not None and self.dialogo.avanzar(evento):
            self.dialogo = None
            self.reproductor.completar_dialogo()

    def update(self, delta: float) -> None:
        self.tiempo_escena += delta
        for actor_id, animacion in self.animaciones.items():
            if self.actores[actor_id]["visible"]:
                animacion.update(delta)
        if self.dialogo is not None:
            self.dialogo.update(delta)
        self.reproductor.update(delta, self._procesar_evento)

    def draw(self, pantalla: pygame.Surface) -> None:
        self.habitacion_renderer.dibujar_fondo(pantalla)
        elementos = [
            elemento for elemento in self.habitacion["props"]
            if elemento["id"] not in ("window", "bed")
        ]
        for elemento in sorted(elementos, key=lambda item: int(item["layer"])):
            self._dibujar_elemento(pantalla, elemento)

        self.habitacion_renderer.dibujar_sombras(pantalla, list(self.actores.values()))
        for actor in sorted(self.actores.values(), key=lambda item: int(item["layer"])):
            if not actor["visible"]:
                continue
            self.animaciones[str(actor["id"])].seleccionar(str(actor["animacion"]))
            self.animaciones[str(actor["id"])].dibujar(
                pantalla,
                (int(actor["x"]), int(actor["y"])),
                (int(actor["width"]), int(actor["height"])),
            )

        self.habitacion_renderer.dibujar_iluminacion_y_efectos(pantalla, self.tiempo_escena)

        if self.dialogo is not None:
            texto_ayuda = "dialogue_continue_two_players" if estado_juego.cantidad_jugadores == 2 else "dialogue_continue"
            self.dialogo.dibujar(
                pantalla,
                self.fuente_dialogo,
                self.textos["ui"][texto_ayuda],
            )
        if SALTAR_CINEMATICA_HABILITADO:
            ayuda = self.gestor.fuente.render(self.textos["ui"]["cinematic_skip"], True, (166, 160, 144))
            pantalla.blit(ayuda, (ANCHO_PANTALLA - ayuda.get_width() - 22, 18))

        if self.reproductor.opacidad:
            negro = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
            negro.fill((0, 0, 0))
            negro.set_alpha(self.reproductor.opacidad)
            pantalla.blit(negro, (0, 0))

    def _procesar_evento(self, evento: dict[str, object]) -> None:
        tipo = str(evento["tipo"]).upper()
        if tipo == "MOSTRAR_PERSONAJE":
            actor = self.actores[str(evento["personaje"])]
            actor["visible"] = True
        elif tipo == "MOVER":
            actor = self.actores[str(evento["personaje"])]
            posicion = evento["posicion"]
            actor["x"], actor["y"] = int(posicion[0]), int(posicion[1])
        elif tipo in ("DIALOGO", "DIALOGO_SIMULTANEO"):
            linea = {
                "speaker": self.textos["names"][str(evento["nombre_key"])],
                "text": self._resolver_texto(str(evento["texto_key"])),
            }
            self.dialogo = DialogueBox([linea])
        elif tipo == "SONIDO_AMBIENTE":
            sonidos = evento.get("sonidos", [])
            self.audio.reproducir_ambientes([str(nombre) for nombre in sonidos])
        elif tipo == "CAMBIAR_ESCENA":
            destinos = {"scene_2": Escena2Pendiente}
            self.audio.detener_ambientes()
            self.gestor.change_scene(destinos[str(evento["destino"])])

    def _resolver_texto(self, ruta: str) -> str:
        valor: object = self.textos["cinematics"]["dialogues"]
        for parte in ruta.split("."):
            valor = valor[parte]
        return str(valor)

    def _dibujar_elemento(self, pantalla: pygame.Surface, elemento: dict[str, object]) -> None:
        rect = pygame.Rect(
            int(elemento["x"]),
            int(elemento["y"]),
            int(elemento["width"]),
            int(elemento["height"]),
        )
        imagen = CARGADOR_ASSETS.imagen(str(elemento["sprite"]))
        if imagen is not None:
            pantalla.blit(CARGADOR_ASSETS.escalar_pixel_perfecto(imagen, rect.size), rect)
            return

        identificador = str(elemento["id"])
        if identificador == "door":
            pygame.draw.rect(pantalla, (25, 28, 26), rect)
            pygame.draw.rect(pantalla, (111, 85, 57), rect, 7)
            pygame.draw.rect(pantalla, (31, 39, 35), rect.inflate(-17, -12))
            pygame.draw.rect(pantalla, (21, 28, 26), (rect.x + 20, rect.y + 31, rect.w - 40, 63))
            pygame.draw.rect(pantalla, (70, 83, 72), (rect.x + 24, rect.y + 35, rect.w - 48, 4))
            pygame.draw.rect(pantalla, (143, 128, 91), (rect.right - 24, rect.centery, 8, 13))
            pygame.draw.rect(pantalla, (81, 45, 38), (rect.x + 20, rect.y + 119, rect.w - 40, 5))
        elif identificador in ("window", "bed"):
            return


class Cinematica1(CinematicScene):
    def __init__(self, gestor) -> None:
        super().__init__(gestor, "cinematic_1", "room_304")