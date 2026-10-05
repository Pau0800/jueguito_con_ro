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

# Parámetros compartidos por la escena lineal del cementerio.
VELOCIDAD_CEMENTERIO = 220.0
DURACION_CEMENTERIO_SEGUNDOS = 50.0
LARGO_NIVEL_CEMENTERIO = int(VELOCIDAD_CEMENTERIO * DURACION_CEMENTERIO_SEGUNDOS)
ALTURA_SUELO_CEMENTERIO = 414
ANCHO_COLLIDER_CEMENTERIO = 24
ALTO_COLLIDER_CEMENTERIO = 42
MARGEN_CAMARA_CEMENTERIO = 96
VELOCIDAD_CAMARA_CEMENTERIO = 8.0
SEGUNDOS_FADE_INTRO_CEMENTERIO = 0.55
SEGUNDOS_FINAL_CEMENTERIO = 3.0
CANTIDAD_TUMBAS_ABIERTAS_CEMENTERIO = 6
DURACION_CARTEL_ADVERTENCIA_CEMENTERIO = 2.8
DURACION_SILUETAS_FINALES_CEMENTERIO = 2.6
FUERZA_SALTO_CEMENTERIO = 590.0
VELOCIDAD_HORIZONTAL_SALTO_CEMENTERIO = 1.18
GRAVEDAD_CEMENTERIO = 1150.0
VELOCIDAD_ANIMACION_CEMENTERIO = 8.0
DURACION_CAIDA_TUMBA = 0.42
DURACION_SALIDA_RESCATE = 0.72
TOQUES_RESCATE_NECESARIOS = 30
SEGUNDOS_RESCATE = 10.0
DISTANCIA_RESCATE = 112

EFECTOS_CEMENTERIO = {
	"iluminacion_habilitada": True,
	"oscuridad_alpha": 138,
	"linterna_habilitada": True,
	"linterna_radio": 210,
	"linterna_intensidad": 0.78,
	"sombras_habilitadas": True,
	"niebla_habilitada": True,
	"niebla_alpha": 26,
	"vineta_habilitada": True,
	"niebla_velocidad_lejana": 7.0,
	"niebla_velocidad_cercana": 15.0,
	"grano_habilitado": True,
	"grano_fps": 8.0,
	"vineta_intensidad": 0.68,
	"grano_intensidad": 0.07,
	"parpadeo_habilitado": True,
	"parpadeo_intensidad": 0.06,
	"parpadeo_frecuencia": 1.4,
}

SILUETAS_FINALES_CEMENTERIO = {
	"cantidad": 2,
	"ancho": 36,
	"alto": 50,
	"amplitud": 8,
	"velocidad": 1.8,
	"desfase": 0.7,
}

INTERVALO_PASOS_CEMENTERIO = 0.36

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

PALETA_CEMENTERIO = {
	"cielo": (13, 19, 22),
	"estrellas": (83, 96, 90),
	"luna_sombra": (56, 68, 66),
	"luna": (139, 142, 117),
	"crater": (107, 116, 99),
	"fondo_lejano": (21, 30, 30),
	"fondo_piedra": (35, 43, 39),
	"suelo": (39, 43, 38),
	"tierra": (56, 49, 38),
	"sombra": (17, 19, 17),
	"piedra": (46, 52, 48),
	"piedra_luz": (86, 88, 70),
	"grabado": (99, 85, 65),
	"nicho": (31, 38, 36),
	"metal": (82, 76, 61),
	"pozo": (10, 12, 12),
	"borde_pozo": (79, 53, 37),
	"niebla": (106, 116, 106),
	"luz": (0, 0, 0),
	"noche": (5, 8, 10),
	"gameover_velo": (4, 6, 7),
	"gameover_titulo": (208, 199, 183),
	"gameover_texto": (184, 180, 169),
	"gameover_ayuda": (151, 156, 150),
	"indicador_activo": (210, 194, 151),
	"indicador_inactivo": (130, 133, 125),
	"nicho_fondo": (16, 23, 24),
	"arbol": (20, 28, 28),
	"arbol_borde": (51, 58, 48),
	"debug_pozo": (255, 160, 30),
	"debug_colision": (220, 35, 45),
	"debug_jugador": (70, 235, 120),
	"debug_texto": (221, 213, 190),
	"pozo_sombra": (27, 29, 26),
	"lapida_final": (51, 56, 51),
	"lapida_final_linea": (120, 111, 82),
	"plataforma_final": (50, 47, 39),
	"plataforma_borde": (105, 89, 65),
	"cuerpo": (25, 29, 27),
	"cuerpo_ropa": (47, 54, 48),
	"cuerpo_piel": (81, 70, 56),
	"cuerpo_luz": (104, 94, 72),
	"barra_fondo": (41, 42, 37),
	"barra_borde": (115, 106, 83),
	"panel_ui": (12, 15, 15),
	"panel_borde": (91, 83, 66),
	"ui_desactivada": (121, 105, 77),
	"ui_inactiva": (143, 146, 139),
	"grano": (103, 131, 159, 184),
	"texto": (215, 207, 183),
	"acento": (124, 102, 67),
}

CAPAS_CEMENTERIO = (
	"fondo",
	"obstaculos",
	"sombras",
	"personajes",
	"iluminacion_efectos",
	"interfaz",
	"fade",
)

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
	"viento": 0.28,
	"grillos": 0.20,
}

ASSETS_AUDIO = {
	"murmullos_hospital": ("audio/ambiente/murmullos_hospital.ogg", "ambiente"),
	"zumbido_fluorescente": ("audio/ambiente/zumbido_fluorescente.ogg", "zumbido"),
	"gotera": ("audio/ambiente/gotera.ogg", "gotera"),
	"pasos": ("audio/sfx/pasos.wav", "sfx"),
	"viento_cementerio": ("audio/ambiente/viento_cementerio.ogg", "viento"),
	"grillos": ("audio/ambiente/grillos.ogg", "grillos"),
	"pasos_tierra": ("audio/sfx/pasos_tierra.ogg", "sfx"),
	"salto": ("audio/sfx/salto.wav", "sfx"),
	"caida_tumba": ("audio/sfx/caida_tumba.wav", "sfx"),
	"rescate": ("audio/sfx/rescate.wav", "sfx"),
}

SONIDOS_AUDIO_HOSPITAL = (
	"murmullos_hospital",
	"zumbido_fluorescente",
	"gotera",
	"pasos",
)