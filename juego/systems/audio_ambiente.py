"""Audio opcional para loops ambientales y pasos."""

from pathlib import Path

import pygame

from juego.config import ASSETS_AUDIO, SONIDOS_AUDIO_HOSPITAL, VOLUMENES_AUDIO


class AudioAmbiente:
    def __init__(self, nombres_sonidos: tuple[str, ...] | None = None) -> None:
        self.ultima_huella = 0.0
        self.sonidos: dict[str, pygame.mixer.Sound] = {}
        self.canales: dict[str, pygame.mixer.Channel] = {}
        self._avisos_emitidos: set[str] = set()
        self.disponible = False
        raiz = Path(__file__).resolve().parents[2] / "assets"
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.set_num_channels(max(pygame.mixer.get_num_channels(), 12))
            self.disponible = True
            nombres = SONIDOS_AUDIO_HOSPITAL if nombres_sonidos is None else nombres_sonidos
            for nombre in nombres:
                if nombre not in ASSETS_AUDIO:
                    print(f"Audio configurado desconocido: '{nombre}'.")
                    continue
                ruta_relativa, canal_nombre = ASSETS_AUDIO[nombre]
                ruta = raiz / ruta_relativa
                if not ruta.is_file():
                    self._avisar_faltante(nombre, ruta_relativa)
                    continue
                try:
                    sonido = pygame.mixer.Sound(str(ruta))
                except pygame.error as error:
                    print(f"No se pudo cargar audio '{nombre}' ({ruta_relativa}): {error}")
                    continue
                sonido.set_volume(float(VOLUMENES_AUDIO[canal_nombre]))
                self.sonidos[nombre] = sonido
        except pygame.error:
            self.disponible = False
            print("Audio no disponible: no se pudo inicializar el mezclador de Pygame.")

    def _avisar_faltante(self, nombre: str, ruta: str) -> None:
        if nombre not in self._avisos_emitidos:
            print(f"Audio opcional ausente: {ruta} ({nombre}); se continúa sin sonido.")
            self._avisos_emitidos.add(nombre)

    def reproducir_ambientes(self, nombres: list[str]) -> None:
        """Inicia en loop los ambientes indicados y detiene los anteriores."""
        if not self.disponible:
            return
        self.detener_ambientes()
        for indice, nombre in enumerate(nombres):
            if nombre not in ASSETS_AUDIO:
                print(f"Audio ambiente desconocido: '{nombre}'.")
                continue
            ruta, canal_nombre = ASSETS_AUDIO[nombre]
            sonido = self.sonidos.get(nombre)
            if sonido is None:
                self._avisar_faltante(nombre, ruta)
                continue
            canal = pygame.mixer.Channel(indice)
            canal.set_volume(float(VOLUMENES_AUDIO[canal_nombre]))
            canal.play(sonido, loops=-1)
            self.canales[nombre] = canal

    def detener_ambientes(self) -> None:
        for canal in self.canales.values():
            canal.stop()
        self.canales.clear()

    def reproducir_sfx(self, nombre: str) -> None:
        if not self.disponible:
            return
        sonido = self.sonidos.get(nombre)
        if sonido is None:
            ruta = ASSETS_AUDIO.get(nombre, (f"audio/sfx/{nombre}.wav", "sfx"))[0]
            self._avisar_faltante(nombre, ruta)
            return
        sonido.set_volume(float(VOLUMENES_AUDIO["sfx"]))
        sonido.play()

    def actualizar(self, delta: float, hay_pasos: bool) -> None:
        self.ultima_huella -= delta
        if hay_pasos and self.ultima_huella <= 0:
            self.reproducir_sfx("pasos")
            self.ultima_huella = 0.32


AudioManager = AudioAmbiente