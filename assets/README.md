# Assets de terror pixel art

La Cinemática 1 carga estos PNG mediante `AssetLoader` con caché. Los placeholders incluidos usan una paleta apagada y vecino más cercano; puedes reemplazar cada PNG conservando la ruta/nombre sin cambiar Python. La resolución de escena existente se mantiene en **960 x 540**.

## Personajes

Cada personaje tiene `assets/sprites/personajes/<nombre>/atlas.png`, transparente, **128 x 288 px**. Celda: **32 x 48 px**; 4 columnas x 6 filas.

| Fila | Contenido |
|---|---|
| 1 | `idle`: respiración sutil, pies quietos |
| 2 | `walk_down`: abajo, 4 pasos |
| 3 | `walk_left`: izquierda, 4 pasos |
| 4 | `walk_right`: derecha, 4 pasos |
| 5 | `walk_up`: arriba, 4 pasos |
| 6 | `sentada`: pose sentada; 4 frames de respiración |

Cada celda ocupa 32 x 48 px. Mantén el personaje centrado y deja transparencia alrededor para que no cambie el encuadre. El loader admite spritesheets del mismo formato; el tamaño de celda y FPS se configuran en `juego/config.py`.

Archivos mínimos para las siguientes etapas:

- `sprites/personajes/chica_1/atlas.png`, `chica_2/atlas.png`: chalecos de fuerza en la fila sentada.
- `sprites/personajes/periodista_1/atlas.png`, `periodista_2/atlas.png`.
- `sprites/personajes/sereno_1/atlas.png`, `sereno_2/atlas.png`.
- `sprites/personajes/sectario_1/atlas.png`, `sectario_2/atlas.png`.

Todos usan la misma celda y orden de filas, para compartir `SpriteAnimado`.

## Habitación 304

Las capas PNG miden **960 x 540 px** y se superponen en este orden: pared, piso, props. Conserva transparencia en `piso.png` y `props.png`.

- `fondos/habitacion/room_304/pared.png`: pared descascarada, humedad, grietas, zócalos, ventana, cuadros y carteles.
- `fondos/habitacion/room_304/piso.png`: baldosas gastadas, manchas y grietas; alfa en la zona de pared.
- `fondos/habitacion/room_304/props.png`: fluorescentes, camilla, radiador, objetos caídos y desgaste. Puede ser transparente.
- `sprites/props/puerta_habitacion.png`: puerta completa con marco, ventanilla, cerradura y desgaste, destino 118 x 342 px.
- `sprites/props/cama_hospital.png`: camilla, destino 260 x 112 px.
- `sprites/props/ventana_rejas.png`: ventana enrejada, destino 156 x 104 px.

La posición, tamaño y capa de puerta/camilla/ventana se define en `data/textos.json`. Los props fallback se dibujan si falta el PNG.

## Tiles y texturas reutilizables

Para extender habitaciones y escenas sin dibujar fondos enteros:

- `fondos/habitacion/tiles_piso.png`: tileset de **256 x 128 px**, celdas 32 x 32 (8 x 4); baldosas, juntas, humedad y desgaste.
- `fondos/habitacion/tiles_pared.png`: **256 x 128 px**, celdas 32 x 32; pared clínica, desconchados, zócalos y variaciones.
- `efectos/texturas/suciedad.png`: **128 x 128 px**, cuatro tiles de 64 x 64 con transparencia.
- `efectos/texturas/grietas.png`: **128 x 128 px**, cuatro decals de 64 x 64 transparentes.
- `sprites/props/fluorescente.png`: **128 x 32 px**, cuerpo y tubo en pixel art.
- Props hospitalarios (cuadro, cartel, radiador, silla de ruedas, frascos): PNG transparente, lienzo recomendado **128 x 96 px** cada uno.

## Audio opcional

Los audios aún no existen en el proyecto. El juego sigue sin sonido cuando falten y lo indica en consola.

- `audio/ambiente/murmullos_hospital.ogg`: loop estéreo, 44.1 kHz.
- `audio/ambiente/zumbido_fluorescente.ogg`: loop mono o estéreo, 44.1 kHz.
- `audio/ambiente/gotera.ogg`: loop corto, mono, 44.1 kHz.
- `audio/sfx/pasos.wav`: pasos cortos, mono, 22.05 kHz.

## Ajustes

En `juego/config.py` puedes ajustar `PALETA_TERROR`, `TAMANO_CELDA_PERSONAJE`, `FPS_ANIMACION_PERSONAJE` y `VOLUMENES_AUDIO`. Los interruptores y parámetros de efectos están agrupados en `EFECTOS_CINEMATICA`: `iluminacion_habilitada`, `halo_personajes_habilitado`, `luz_puerta_habilitada`, `sombras_habilitadas`, `vineta_habilitada`, `grano_habilitado` y `parpadeo_habilitado`. Cada efecto tiene intensidad, radio o frecuencia al lado. Para apagar uno, cambia su valor a `False`; para regularlo, ajusta su número.

## Cementerio

La Escena 2 genera pixel-art temporal si faltan los PNG. Las capas se cargan por `AssetLoader` y se pueden sustituir manteniendo estos nombres:

- `fondos/cementerio/cielo.png`: 960 x 540 px, cielo nocturno y luna.
- `fondos/cementerio/fondo_medio.png`: 1920 x 540 px, PNG transparente con árboles secos, rejas y nichos lejanos; parallax lento.
- `fondos/cementerio/suelo.png`: 1920 x 540 px, PNG transparente fuera de la zona de tierra; parallax cercano.
- `sprites/personajes/sereno_1/atlas.png` y `sereno_2/atlas.png`: 128 x 288 px, celdas de 32 x 48 px. Se usan filas `idle`, `walk_down`, `walk_left`, `walk_right`, `walk_up`, `sentada`; la animación lateral usa `walk_right` reflejada para la izquierda.
- `audio/ambiente/viento_cementerio.ogg` y `grillos.ogg`: loops opcionales.
- `audio/sfx/pasos_tierra.ogg`, `salto.wav`, `caida_tumba.wav` y `rescate.wav`: efectos opcionales.

El recorrido editable está en `data/nivel_cementerio.json`. Sus elementos usan `tipo`, `x`, `ancho` y, para obstáculos sólidos, `alto`. La velocidad, duración aproximada, salto, rescate y efectos se ajustan en `juego/config.py`.

Para cada atlas de sereno usa cuatro columnas por seis filas; cada fila contiene cuatro frames en el orden indicado arriba. Mantén la figura centrada en la celda y con transparencia alrededor para que el collider de 24 x 42 px no cambie al reemplazar el arte.

Los clips ausentes no interrumpen el juego; el `AudioManager` avisa en consola y la escena sigue sin sonido. Sus canales de volumen y efectos atmosféricos están en `juego/config.py`.
