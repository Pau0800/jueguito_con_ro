# Capas del cementerio

La Escena 2 carga estas capas opcionales desde el cargador central con caché. Si no están, usa fondos pixelados procedurales.

- `cielo.png`: 960 x 540 px, capa opaca con luna/estrellas.
- `fondo_medio.png`: 1920 x 540 px, PNG transparente con siluetas lejanas; se desplaza lentamente.
- `suelo.png`: 1920 x 540 px, PNG transparente por encima del horizonte, con tierra, tumbas lejanas o rejas cercanas.

Usa píxeles sin suavizado y la paleta apagada del hospital. Las capas repetibles deben continuar limpiamente en los bordes izquierdo y derecho.