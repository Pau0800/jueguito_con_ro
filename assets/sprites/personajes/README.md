# Atlas de personajes

Los serenos de la Escena 2 se cargan desde `sereno_1/atlas.png` y `sereno_2/atlas.png`. Si falta el PNG, el juego crea un sprite temporal; para reemplazarlo conserva la ruta y el tamaño.

- Atlas transparente: 128 x 288 px.
- Celda: 32 x 48 px; 4 columnas x 6 filas.
- Filas, de arriba hacia abajo: `idle`, `walk_down`, `walk_left`, `walk_right`, `walk_up`, `sentada`.
- Cuatro frames por fila, en orden temporal; idle y sentada deben animar respiración sutil.

La Escena 2 refleja horizontalmente `walk_right` al moverse a la izquierda. Mantén la figura centrada y dentro de la celda para conservar el collider compartido.