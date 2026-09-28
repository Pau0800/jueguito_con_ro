"""Audio opcional para loops ambientales y pasos."""

from pathlib import Path

import pygame


class AudioAmbiente:
    def __init__(self) -> None:
        self.ultima_huella = 0.0
        self.pasos: pygame.mixer.Sound | None = None
        carpeta = Path(__file__).resolve().parents[2] / "assets" / "audio"
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            ambiente = carpeta / "ambiente_hospital.ogg"
            pasos = carpeta / "pasos.wav"
            if ambiente.exists():
                pygame.mixer.music.load(str(ambiente))
                pygame.mixer.music.set_volume(0.38)
                pygame.mixer.music.play(-1)
            if pasos.exists():
                self.pasos = pygame.mixer.Sound(str(pasos))
                self.pasos.set_volume(0.5)
        except pygame.error:
            self.pasos = None

    def actualizar(self, delta: float, hay_pasos: bool) -> None:
        self.ultima_huella -= delta
        if hay_pasos and self.pasos is not None and self.ultima_huella <= 0:
            self.pasos.play()
            self.ultima_huella = 0.32