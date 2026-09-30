"""Caja de diálogo reutilizable por escenas y cinemáticas."""

import pygame

from juego.config import VELOCIDAD_TEXTO_DIALOGO
from juego.systems.fonts import cargar_fuente


class DialogueBox:
    def __init__(
        self,
        lineas: list[dict[str, str]],
        velocidad_texto: float = VELOCIDAD_TEXTO_DIALOGO,
    ) -> None:
        self.lineas = lineas
        self.indice = 0
        self.activo = bool(lineas)
        self.velocidad_texto = velocidad_texto
        self.caracteres_visibles = 0.0

    def update(self, delta: float) -> None:
        linea = self.linea_actual
        if linea is not None:
            self.caracteres_visibles = min(
                float(len(linea["text"])),
                self.caracteres_visibles + self.velocidad_texto * delta,
            )

    @property
    def linea_actual(self) -> dict[str, str] | None:
        if not self.activo:
            return None
        return self.lineas[self.indice]

    def avanzar(self, evento: pygame.event.Event) -> bool:
        """Completa el tipeo o avanza; devuelve True cuando termina el bloque."""
        if not self.activo or not self._es_accion(evento):
            return False
        linea = self.linea_actual
        if linea is not None and self.caracteres_visibles < len(linea["text"]):
            self.caracteres_visibles = float(len(linea["text"]))
            return False
        self.indice += 1
        if self.indice >= len(self.lineas):
            self.activo = False
            return True
        self.caracteres_visibles = 0.0
        return False

    @staticmethod
    def _es_accion(evento: pygame.event.Event) -> bool:
        if evento.type == pygame.KEYDOWN:
            return evento.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE)
        return evento.type == pygame.JOYBUTTONDOWN and evento.button == 0

    def dibujar(self, pantalla: pygame.Surface, fuente: pygame.font.Font, ayuda: str) -> None:
        linea = self.linea_actual
        if linea is None:
            return
        caja = pygame.Rect(38, 390, 884, 120)
        pygame.draw.rect(pantalla, (14, 16, 18), caja)
        pygame.draw.rect(pantalla, (116, 119, 111), caja, 2)
        nombre = fuente.render(linea["speaker"], True, (205, 190, 154))
        texto = fuente.render(linea["text"][: int(self.caracteres_visibles)], True, (230, 226, 211))
        indicacion = cargar_fuente(20).render(ayuda, True, (143, 146, 139))
        pantalla.blit(nombre, (caja.x + 18, caja.y + 13))
        pantalla.blit(texto, (caja.x + 18, caja.y + 43))
        pantalla.blit(indicacion, (caja.right - indicacion.get_width() - 18, caja.bottom - 25))