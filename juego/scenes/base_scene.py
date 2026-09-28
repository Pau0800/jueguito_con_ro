"""Interfaz común de una escena."""


class BaseScene:
    def __init__(self, gestor) -> None:
        self.gestor = gestor
        self.textos = gestor.textos

    def handle_event(self, _evento) -> None:
        del _evento
        raise NotImplementedError

    def update(self, _delta: float) -> None:
        del _delta
        raise NotImplementedError

    def draw(self, _pantalla) -> None:
        del _pantalla
        raise NotImplementedError