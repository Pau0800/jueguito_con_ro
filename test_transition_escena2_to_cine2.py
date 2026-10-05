#!python3.13
"""Prueba de integración: llegada de serenos a la tumba final en EscenaCementerio
y transición automática hacia Cinemática 2."""

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from juego.scene_manager import SceneManager
from juego.scenes.escena_cementerio import EscenaCementerio
from juego.scenes.cinematica_2 import Cinematica2


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((960, 540))
    gestor = SceneManager(pantalla)

    print("=== INICIANDO PRUEBA DE TRANSICIÓN ESCENA 2 -> CINEMÁTICA 2 ===")
    gestor.start(EscenaCementerio)
    escena = gestor.escena

    # Saltar intro de diálogo si existe
    if escena.dialogo is not None:
        escena.dialogo = None
        escena.fase = "jugando"

    # Posicionar a los jugadores justo en la meta final
    x_meta = int(escena.datos_nivel["tumba_final_x"]) + 10
    for jugador in escena.jugadores:
        jugador.rect.x = x_meta
        jugador.posicion_x = float(x_meta)

    # Actualizar la escena para que detecte la llegada
    delta = 0.05
    tiempo = 0.0
    fase_final_detectada = False
    cinematica2_iniciada = False

    while tiempo < 5.0:
        gestor.update(delta)
        tiempo += delta

        if isinstance(gestor.escena, EscenaCementerio) and gestor.escena.fase == "final":
            if not fase_final_detectada:
                print(f"[t={tiempo:.2f}s] Serenos llegaron a la tumba final. Fase 'final' activa (cuerpos visibles).")
                fase_final_detectada = True
        elif isinstance(gestor.escena, Cinematica2):
            if not cinematica2_iniciada:
                print(f"[t={tiempo:.2f}s] ¡Transición completada! Cinemática 2 iniciada con éxito.")
                cinematica2_iniciada = True
                break

    pygame.quit()

    assert fase_final_detectada, "No se detectó la fase 'final' al llegar a la tumba"
    assert cinematica2_iniciada, "No se activó Cinematica2 después del fundido"
    print("=== TRANSICIÓN VERIFICADA Y FUNCIONANDO CORRECTAMENTE ===")


if __name__ == "__main__":
    main()
