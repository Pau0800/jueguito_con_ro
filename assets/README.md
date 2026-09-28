# Assets del juego

Los fondos y personajes de prueba se generan con formas pixeladas en Python. Al colocar los archivos con estos nombres, el juego los carga automáticamente y conserva sus sistemas de movimiento e interacción.

## Sprites

- `sprites/players/atlas_periodista_1.png` y `atlas_periodista_2.png`: atlas PNG transparente de **64 x 96 px**. Cada celda mide **16 x 24 px**. Cuatro columnas: reposo, paso A, paso B, paso C. Cuatro filas: abajo, izquierda, derecha, arriba.
- Dibujar siluetas legibles a escala pequeña, con contorno oscuro y paleta apagada. El juego escala cada fotograma con vecino más cercano.

## Fondos

- `images/backgrounds/menu_hospital.png`: ilustración del menú, **320 x 180 px**.
- `images/backgrounds/recepcion.png`, `sala1.png`, `sala2.png`: fondos de escenario, **960 x 540 px**.
- Se recomienda conservar paredes, suelo y mobiliario integrados en cada fondo; puertas interactivas y personajes se dibujan por encima.

## Sonido y fuentes

- `audio/ambiente_hospital.ogg`: loop estéreo de ambiente (zumbido fluorescente y murmullos), 44.1 kHz.
- `audio/pasos.wav`: paso corto mono, 22.05 kHz; se reproduce en intervalos durante el movimiento.
- `fonts/pixel.ttf`: fuente pixel legible, compatible con Pygame/SDL_ttf.

El audio es opcional: si falta, el juego sigue funcionando sin sonido. La referencia visual es una dirección de pixel art de terror original, no una copia de sprites o escenarios existentes.