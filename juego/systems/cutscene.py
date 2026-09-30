"""Reproductor por datos para cinemáticas y eventos de escena."""

from collections.abc import Callable


class CinematicPlayer:
    """Ejecuta eventos en orden y se detiene en esperas o diálogos."""

    def __init__(self, eventos: list[dict[str, object]], duraciones: dict[str, float]) -> None:
        self.eventos = eventos
        self.duraciones = duraciones
        self.indice = 0
        self.tiempo_evento = 0.0
        self.opacidad = 255
        self.evento_dialogo_activo = False
        self.terminada = not eventos

    @property
    def evento_actual(self) -> dict[str, object] | None:
        if self.terminada:
            return None
        return self.eventos[self.indice]

    def update(self, delta: float, procesar_evento: Callable[[dict[str, object]], None]) -> None:
        while not self.terminada:
            evento = self.eventos[self.indice]
            tipo = str(evento["tipo"]).upper()

            if tipo in ("FADE_IN", "FADE_OUT", "ESPERAR"):
                duracion = self._duracion(evento)
                self.tiempo_evento += delta
                progreso = min(1.0, self.tiempo_evento / duracion) if duracion > 0 else 1.0
                if tipo == "FADE_IN":
                    self.opacidad = round(255 * (1.0 - progreso))
                elif tipo == "FADE_OUT":
                    self.opacidad = round(255 * progreso)
                if progreso < 1.0:
                    return
                if tipo == "FADE_IN":
                    self.opacidad = 0
                elif tipo == "FADE_OUT":
                    self.opacidad = 255
                self._avanzar_evento()
                return

            if tipo in ("DIALOGO", "DIALOGO_SIMULTANEO"):
                if not self.evento_dialogo_activo:
                    procesar_evento(evento)
                    self.evento_dialogo_activo = True
                return

            if tipo in ("MOSTRAR_PERSONAJE", "MOVER", "SONIDO_AMBIENTE", "CAMBIAR_ESCENA"):
                procesar_evento(evento)
                self._avanzar_evento()
                if tipo == "CAMBIAR_ESCENA":
                    return
                continue

            raise ValueError(f"Tipo de evento cinematográfico desconocido: {tipo}")

    def completar_dialogo(self) -> None:
        if self.evento_dialogo_activo:
            self._avanzar_evento()

    def _duracion(self, evento: dict[str, object]) -> float:
        clave = evento.get("duracion_config")
        if clave is not None:
            return float(self.duraciones[str(clave)])
        return float(evento.get("segundos", 0.0))

    def _avanzar_evento(self) -> None:
        self.indice += 1
        self.tiempo_evento = 0.0
        self.evento_dialogo_activo = False
        self.terminada = self.indice >= len(self.eventos)


# Mantiene compatibilidad con código que usaba el nombre previo.
CutscenePlayer = CinematicPlayer