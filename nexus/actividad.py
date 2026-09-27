"""Registro de lo que Bárbara va haciendo: cuándo publica y de dónde llegan las visitas a su tarjeta.

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
        return {"publicaciones": [], "visitas": {}}


def _guardar(actividad: dict) -> None:
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(actividad, ensure_ascii=False, indent=2), encoding="utf-8")


def registrar_publicacion(actividad: dict, hoy: date) -> None:
    actividad["publicaciones"].append(hoy.isoformat())
    _guardar(actividad)


def registrar_visita(actividad: dict, origen: str | None) -> None:
    """Cuenta una visita a la tarjeta digital según de dónde llegó (el QR o link que usó)."""
    visitas = actividad.setdefault("visitas", {})
    origen = origen or "Link directo"
    visitas[origen] = visitas.get(origen, 0) + 1
    _guardar(actividad)


def dias_sin_publicar(actividad: dict, hoy: date) -> int | None:
    """Días desde la última publicación registrada, o None si nunca registró una."""
    if not actividad["publicaciones"]:
        return None
    return (hoy - date.fromisoformat(max(actividad["publicaciones"]))).days
