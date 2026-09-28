"""Reproductor mínimo de eventos declarativos para futuras cinemáticas."""

from collections.abc import Callable


class CutscenePlayer:
    """Procesa eventos de espera, diálogo y movimiento en orden."""

    def __init__(self, eventos: list[dict[str, object]]) -> None:
        self.eventos = eventos
        self.indice = 0
        self.tiempo_evento = 0.0
        self.dialogo_visible = False
        self.terminada = not eventos

    def update(
        self,
        delta: float,
        mostrar_dialogo: Callable[[str, str], None],
        mover_personaje: Callable[[str, tuple[int, int]], None],
    ) -> None:
        if self.terminada:
            return

        evento = self.eventos[self.indice]
        tipo = evento["tipo"]
        if tipo == "esperar":
            self.tiempo_evento += delta
            if self.tiempo_evento >= float(evento.get("segundos", 0)):
                self._avanzar_evento()
            return
        elif tipo == "dialogo":
            if not self.dialogo_visible:
                mostrar_dialogo(str(evento["personaje"]), str(evento["texto"]))
                self.dialogo_visible = True
            return
        elif tipo == "mover":
            posicion = evento["posicion"]
            mover_personaje(str(evento["personaje"]), (int(posicion[0]), int(posicion[1])))
            self._avanzar_evento()
            return
        else:
            raise ValueError(f"Tipo de evento de cinemática desconocido: {tipo}")

    def continuar_dialogo(self) -> bool:
        """Confirma el diálogo activo y permite continuar la secuencia."""
        if self.terminada or not self.dialogo_visible:
            return False
        self._avanzar_evento()
        return True

    def _avanzar_evento(self) -> None:
        self.indice += 1
        self.tiempo_evento = 0.0
        self.dialogo_visible = False
        self.terminada = self.indice >= len(self.eventos)