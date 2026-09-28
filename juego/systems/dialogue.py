"""Caja de diálogo reutilizable por escenas y cinemáticas."""

import pygame

from juego.systems.fonts import cargar_fuente
from juego.systems.input import accion_presionada


class DialogueBox:
    def __init__(self, lineas: list[dict[str, str]]) -> None:
        self.lineas = lineas
        self.indice = 0
        self.activo = bool(lineas)

    @property
    def linea_actual(self) -> dict[str, str] | None:
        if not self.activo:
            return None
        return self.lineas[self.indice]

    def avanzar(self, evento: pygame.event.Event) -> bool:
        """Avanza una línea; devuelve True al terminar el diálogo."""
        if not self.activo or not accion_presionada(evento):
            return False
        self.indice += 1
        if self.indice >= len(self.lineas):
            self.activo = False
            return True
        return False

    def dibujar(self, pantalla: pygame.Surface, fuente: pygame.font.Font, ayuda: str) -> None:
        linea = self.linea_actual
        if linea is None:
            return
        caja = pygame.Rect(38, 390, 884, 120)
        pygame.draw.rect(pantalla, (14, 16, 18), caja)
        pygame.draw.rect(pantalla, (116, 119, 111), caja, 2)
        nombre = fuente.render(linea["speaker"], True, (205, 190, 154))
        texto = fuente.render(linea["text"], True, (230, 226, 211))
        indicacion = cargar_fuente(20).render(ayuda, True, (143, 146, 139))
        pantalla.blit(nombre, (caja.x + 18, caja.y + 13))
        pantalla.blit(texto, (caja.x + 18, caja.y + 43))
        pantalla.blit(indicacion, (caja.right - indicacion.get_width() - 18, caja.bottom - 25))