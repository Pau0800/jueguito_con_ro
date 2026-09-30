"""Ajustes rápidos del prototipo."""

ANCHO_PANTALLA = 960
ALTO_PANTALLA = 540
FPS = 60
TIEMPO_BUSQUEDA_SEGUNDOS = 50
CANTIDAD_PUERTAS_SALA_1 = 4
CANTIDAD_PUERTAS_SALA_2 = 3

TECLA_INTERACCION = "E"
VELOCIDAD_JUGADOR = 220
VELOCIDAD_TEXTO_DIALOGO = 42
DURACION_FADE_CINEMATICA = 1.0
DURACION_ESPERA_CINEMATICA = 0.55
SALTAR_CINEMATICA_HABILITADO = True
TECLA_SALTAR_CINEMATICA = "escape"

# La ventana y las escenas ya usan 960x540; se conserva esa resolución.
RESOLUCION_INTERNA = (ANCHO_PANTALLA, ALTO_PANTALLA)
ESCALA_PIXEL_ART = 2
TAMANO_CELDA_PERSONAJE = (32, 48)
FRAMES_POR_ANIMACION = 4
FPS_ANIMACION_PERSONAJE = 7.0

PALETA_TERROR = {
	"negro": (10, 12, 11),
	"sombra": (20, 24, 22),
	"pared": (48, 54, 46),
	"pared_clara": (69, 68, 53),
	"humedad": (31, 43, 39),
	"piso": (39, 43, 38),
	"baldosa": (57, 59, 49),
	"madera": (82, 62, 46),
	"metal": (87, 94, 83),
	"tela": (126, 120, 98),
	"piel": (174, 143, 117),
	"rojo_sucio": (111, 49, 43),
	"luz": (177, 184, 143),
	"texto": (220, 211, 187),
}

CAPAS_HABITACION = (
	"fondo",
	"pared",
	"piso",
	"props",
	"sombras",
	"personajes",
	"iluminacion",
	"efectos",
	"interfaz",
	"fade",
)

EFECTOS_CINEMATICA = {
	"iluminacion_habilitada": True,
	"oscuridad_alpha": 92,
	"halo_personajes_habilitado": True,
	"halo_radio": 118,
	"halo_intensidad": 0.62,
	"luz_puerta_habilitada": True,
	"luz_puerta_posicion": (846, 244),
	"luz_puerta_radio": 176,
	"luz_puerta_intensidad": 0.55,
	"sombras_habilitadas": True,
	"vineta_habilitada": True,
	"vineta_intensidad": 0.62,
	"grano_habilitado": True,
	"grano_intensidad": 0.09,
	"grano_fps": 8.0,
	"parpadeo_habilitado": True,
	"parpadeo_intensidad": 0.08,
	"parpadeo_frecuencia": 2.4,
}

VOLUMENES_AUDIO = {
	"ambiente": 0.34,
	"zumbido": 0.22,
	"gotera": 0.28,
	"sfx": 0.50,
}

ASSETS_AUDIO = {
	"murmullos_hospital": ("audio/ambiente/murmullos_hospital.ogg", "ambiente"),
	"zumbido_fluorescente": ("audio/ambiente/zumbido_fluorescente.ogg", "zumbido"),
	"gotera": ("audio/ambiente/gotera.ogg", "gotera"),
	"pasos": ("audio/sfx/pasos.wav", "sfx"),
}