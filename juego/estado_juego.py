"""Estado global compartido por las escenas del juego."""


cantidad_jugadores = 1


def definir_cantidad_jugadores(cantidad: int) -> None:
    global cantidad_jugadores
    if cantidad not in (1, 2):
        raise ValueError("La cantidad de jugadores debe ser 1 o 2.")
    cantidad_jugadores = cantidad