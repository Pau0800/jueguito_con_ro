#!python3.13
"""Script de verificación determinista de la Cinemática 2.
Ejecuta la cinemática con SDL_VIDEODRIVER=dummy, guarda capturas en 'capturas_debug'
a los 0 s, 1 s, 3.5 s, 6 s y 9.9 s, y mide los tiempos de cada fase.
"""

import os
import sys
from pathlib import Path

# Configurar drivers dummy antes de inicializar Pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame

from juego.scene_manager import SceneManager
from juego.scenes.cinematica_2 import Cinematica2, TIEMPO_NEGRO, DURACION_CINEMATICA
from juego.scenes.placeholder import SiguienteEscenaPendiente


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((960, 540))
    gestor = SceneManager(pantalla)

    carpeta_debug = Path("capturas_debug")
    carpeta_debug.mkdir(exist_ok=True)

    print("=== INICIANDO PRUEBA DE CINEMÁTICA 2 ===")
    gestor.start(Cinematica2)

    tiempos_captura = [0.0, 1.0, 3.5, 6.0, 9.9]
    capturas_tomadas = set()

    tiempo_actual = 0.0
    delta = 0.05  # Paso fijo de 50 ms

    tiempo_inicio_negro = None
    tiempo_fin_negro = None
    tiempo_inicio_cine = None
    tiempo_fin_cine = None
    tiempo_activacion_siguiente = None

    tiempo_inicio_negro = tiempo_actual

    # Simulamos hasta 10.5 segundos
    while tiempo_actual <= 10.5:
        # Verificar capturas pendientes en el instante actual
        for tc in tiempos_captura:
            if tc not in capturas_tomadas and abs(tiempo_actual - tc) < delta / 2:
                gestor.draw()
                ruta = carpeta_debug / f"captura_{tc:.1f}s.png"
                pygame.image.save(pantalla, str(ruta))
                capturas_tomadas.add(tc)
                print(f"[Captura guardada] {ruta} en t={tiempo_actual:.2f}s")

        # Rastrear cambios de fase
        if isinstance(gestor.escena, Cinematica2):
            cine = gestor.escena
            if cine.tiempo_total < TIEMPO_NEGRO:
                pass
            else:
                if tiempo_fin_negro is None:
                    tiempo_fin_negro = tiempo_actual
                    tiempo_inicio_cine = tiempo_actual
        elif isinstance(gestor.escena, SiguienteEscenaPendiente):
            if tiempo_activacion_siguiente is None:
                tiempo_fin_cine = tiempo_actual
                tiempo_activacion_siguiente = tiempo_actual
                # Captura de la siguiente escena
                gestor.draw()
                ruta_sig = carpeta_debug / "captura_siguiente_escena.png"
                pygame.image.save(pantalla, str(ruta_sig))
                print(f"[Captura guardada] {ruta_sig} en t={tiempo_actual:.2f}s (SiguienteEscenaPendiente)")

        gestor.update(delta)
        tiempo_actual = round(tiempo_actual + delta, 4)

    pygame.quit()

    print("\n=== RESULTADOS DE MEDICIÓN DE TIEMPOS ===")
    duracion_negro = (tiempo_fin_negro - tiempo_inicio_negro) if tiempo_fin_negro else None
    duracion_cine = (tiempo_activacion_siguiente - tiempo_inicio_cine) if (tiempo_activacion_siguiente and tiempo_inicio_cine) else None

    print(f"Inicio etapa negro:       {tiempo_inicio_negro:.2f} s")
    print(f"Fin etapa negro:          {tiempo_fin_negro:.2f} s (Duración: {duracion_negro:.2f} s)")
    print(f"Inicio etapa cinemática:  {tiempo_inicio_cine:.2f} s")
    print(f"Fin etapa cinemática:     {tiempo_fin_cine:.2f} s (Duración: {duracion_cine:.2f} s)")
    print(f"Activación sig. escena:   {tiempo_activacion_siguiente:.2f} s")

    # Verificación de imágenes guardadas
    print("\n=== ANÁLISIS DE CAPTURAS ===")
    for tc in tiempos_captura:
        ruta = carpeta_debug / f"captura_{tc:.1f}s.png"
        if ruta.exists():
            surf = pygame.image.load(str(ruta))
            # Analizar colores
            es_negro = True
            px_count = 0
            for y in range(0, 540, 10):
                for x in range(0, 960, 10):
                    color = surf.get_at((x, y))[:3]
                    if color != (0, 0, 0):
                        es_negro = False
                        px_count += 1
            print(f"Captura {ruta.name}: {'Totalmente NEGRA' if es_negro else f'Contenido VISIBLE (puntos activos analizados: {px_count})'}")

    print("\n=== PRUEBA COMPLETADA CON ÉXITO ===")


if __name__ == "__main__":
    main()
