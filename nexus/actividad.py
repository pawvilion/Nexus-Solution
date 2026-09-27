"""Registro de lo que Bárbara va haciendo (por ahora, cuándo publica).

Responsable: Persona 3.
Se guarda en data/actividad.json, igual que la memoria (fuera de GitHub).
"""

import json
from datetime import date
from pathlib import Path

ARCHIVO = Path(__file__).parent.parent / "data" / "actividad.json"


def cargar() -> dict:
    try:
        return json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"publicaciones": []}


def registrar_publicacion(actividad: dict, hoy: date) -> None:
    actividad["publicaciones"].append(hoy.isoformat())
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(actividad, ensure_ascii=False, indent=2), encoding="utf-8")


def dias_sin_publicar(actividad: dict, hoy: date) -> int | None:
    """Días desde la última publicación registrada, o None si nunca registró una."""
    if not actividad["publicaciones"]:
        return None
    return (hoy - date.fromisoformat(max(actividad["publicaciones"]))).days
