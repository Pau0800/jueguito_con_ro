"""Menú inicial con fondo ilustrado reemplazable."""

import pygame
from pathlib import Path

from juego.scenes.base_scene import BaseScene
from juego.scenes.seleccion_jugadores import SeleccionJugadores
from juego.systems.ambiente import AmbienteHospital
from juego.systems.fonts import cargar_fuente


class MenuInicio(BaseScene):
    def __init__(self, gestor) -> None:
        super().__init__(gestor)
        self.seleccion = 0
        self.fuente_titulo = cargar_fuente(76)
        self.fuente_boton = cargar_fuente(38)
        self.boton_iniciar = pygame.Rect(370, 385, 220, 58)
        ruta_fondo = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "images"
            / "backgrounds"
            / "menu_hospital.png"
        )
        if ruta_fondo.exists():
            imagen = pygame.image.load(str(ruta_fondo))
            if pygame.display.get_surface() is not None:
                imagen = imagen.convert()
            self.fondo = pygame.transform.scale(imagen, (960, 540))
        else:
            self.fondo = self._crear_fondo_temporal()

    @staticmethod
    def _crear_fondo_temporal() -> pygame.Surface:
        """Ilustración pixelada; se reemplaza por assets/menu/fondo.png al existir."""
        fondo_hospital = AmbienteHospital().fondos["sala2"]
        fondo = pygame.transform.scale(fondo_hospital, (320, 180))
        sombra = pygame.Surface((320, 180), pygame.SRCALPHA)
        sombra.fill((3, 7, 7, 112))
        fondo.blit(sombra, (0, 0))
        # Silueta de un umbral profundo en el centro del corredor.
        pygame.draw.rect(fondo, (23, 25, 22), (119, 44, 82, 118))
        pygame.draw.rect(fondo, (101, 76, 53), (119, 44, 82, 7))
        pygame.draw.rect(fondo, (101, 76, 53), (119, 44, 7, 118))
        pygame.draw.rect(fondo, (101, 76, 53), (194, 44, 7, 118))
        pygame.draw.rect(fondo, (12, 15, 15), (132, 55, 55, 107))
        pygame.draw.rect(fondo, (87, 34, 31), (148, 83, 23, 4))
        pygame.draw.rect(fondo, (111, 75, 50), (178, 101, 4, 7))
        pygame.draw.ellipse(fondo, (64, 27, 26), (135, 151, 54, 5))
        return pygame.transform.scale(fondo, (960, 540))

    def handle_event(self, evento: pygame.event.Event) -> None:
        if evento.type == pygame.MOUSEMOTION:
            self.seleccion = 0 if self.boton_iniciar.collidepoint(evento.pos) else -1
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.boton_iniciar.collidepoint(evento.pos):
                self.gestor.change_scene(SeleccionJugadores)
        elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.gestor.change_scene(SeleccionJugadores)

    def update(self, _delta: float) -> None:
        del _delta
        return

    def draw(self, pantalla: pygame.Surface) -> None:
        pantalla.blit(self.fondo, (0, 0))
        velo = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
        velo.fill((5, 8, 8, 105))
        pantalla.blit(velo, (0, 0))
        titulo = self.fuente_titulo.render("EL HOSPITAL", True, (207, 197, 172))
        subtitulo = self.gestor.fuente.render("HISTORIAS QUE NO DEBIERON CONTARSE", True, (141, 143, 126))
        pantalla.blit(titulo, titulo.get_rect(center=(480, 250)))
        pantalla.blit(subtitulo, subtitulo.get_rect(center=(480, 304)))
        self._dibujar_boton(pantalla, self.boton_iniciar, "Iniciar", self.seleccion == 0)

    def _dibujar_boton(
        self, pantalla: pygame.Surface, rectangulo: pygame.Rect, texto: str, activo: bool
    ) -> None:
        color = (91, 83, 66) if activo else (40, 45, 42)
        pygame.draw.rect(pantalla, (14, 17, 17), rectangulo.inflate(8, 8))
        pygame.draw.rect(pantalla, color, rectangulo)
        pygame.draw.rect(pantalla, (144, 128, 94), rectangulo, 2)
        etiqueta = self.fuente_boton.render(texto, True, (224, 215, 190))
        pantalla.blit(etiqueta, etiqueta.get_rect(center=rectangulo.center))