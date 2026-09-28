"""Lectura común de teclado y gamepad."""

import pygame

from juego import estado_juego


def jugador_que_acciona(evento: pygame.event.Event) -> int | None:
    """Devuelve el índice del jugador que pulsó su tecla de interacción."""
    if evento.type == pygame.KEYDOWN:
        if estado_juego.cantidad_jugadores == 1:
            return 0 if evento.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE) else None
        if evento.key == pygame.K_e:
            return 0
        if evento.key == pygame.K_RETURN:
            return 1
    elif evento.type == pygame.JOYBUTTONDOWN and evento.button == 0:
        return 0
    return None


def accion_presionada(evento: pygame.event.Event) -> bool:
    return jugador_que_acciona(evento) is not None


def leer_movimiento(esquema: str = "ambos") -> tuple[float, float]:
    teclas = pygame.key.get_pressed()
    if esquema == "ambos":
        x = float(teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - float(
            teclas[pygame.K_a] or teclas[pygame.K_LEFT]
        )
        y = float(teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - float(
            teclas[pygame.K_w] or teclas[pygame.K_UP]
        )
    elif esquema == "wasd":
        x = float(teclas[pygame.K_d]) - float(teclas[pygame.K_a])
        y = float(teclas[pygame.K_s]) - float(teclas[pygame.K_w])
    elif esquema == "flechas":
        x = float(teclas[pygame.K_RIGHT]) - float(teclas[pygame.K_LEFT])
        y = float(teclas[pygame.K_DOWN]) - float(teclas[pygame.K_UP])
    else:
        raise ValueError(f"Esquema de controles desconocido: {esquema}")

    if esquema in ("ambos", "wasd") and pygame.joystick.get_count():
        mando = pygame.joystick.Joystick(0)
        if not mando.get_init():
            mando.init()
        if mando.get_numaxes() >= 2:
            eje_x, eje_y = mando.get_axis(0), mando.get_axis(1)
            if abs(eje_x) > 0.2 or abs(eje_y) > 0.2:
                x, y = eje_x, eje_y
        if mando.get_numhats():
            hat_x, hat_y = mando.get_hat(0)
            if hat_x or hat_y:
                x, y = float(hat_x), float(-hat_y)

    magnitud = (x * x + y * y) ** 0.5
    if magnitud > 1:
        x, y = x / magnitud, y / magnitud
    return x, y