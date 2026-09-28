"""Carga los textos editables del juego."""

import json
from pathlib import Path
from typing import Any


RUTA_TEXTOS = Path(__file__).resolve().parent.parent / "data" / "textos.json"


def cargar_textos() -> dict[str, Any]:
    with RUTA_TEXTOS.open(encoding="utf-8") as archivo:
        return json.load(archivo)