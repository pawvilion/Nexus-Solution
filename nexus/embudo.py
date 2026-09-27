"""Embudo de clientas: de dónde llegan las consultas y cuántas se convierten en clientas.

Responsable: Persona 3. Idea y primera versión: Benjamín (Marketing Executor).
Solo cantidades anónimas: nunca nombres, teléfonos, RUT ni datos de salud.
Se guarda en data/embudo.json (fuera de GitHub).
"""

import json
from pathlib import Path

ARCHIVO = Path(__file__).parent.parent / "data" / "embudo.json"

# Etapas del embudo, de la primera a la última.
ETAPAS = {
    "consulta": "Me escribió",
    "agendo": "Agendó o compró",
    "volvio": "Volvió otra vez",
}
ORIGENES = ["Instagram", "WhatsApp", "Facebook / Marketplace", "Recomendación", "Feria o afiche (QR)", "Otro"]
SERVICIOS = ["Masajes", "Reiki", "Reflexología", "Aromaterapia", "Flores de Bach", "Guateros y productos", "Otro"]


def cargar() -> list[dict]:
    try:
        return json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def agregar(registros: list[dict], fecha: str, origen: str, servicio: str, etapa: str, cantidad: int) -> None:
    registros.append({"fecha": fecha, "origen": origen.strip() or "Otro", "servicio": servicio,
                      "etapa": etapa, "cantidad": int(cantidad)})
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")


def total(registros: list[dict], etapa: str, origen: str | None = None) -> int:
    return sum(r["cantidad"] for r in registros if r["etapa"] == etapa and (origen is None or r["origen"] == origen))


def conversion(registros: list[dict], origen: str | None = None) -> float | None:
    """Porcentaje de consultas que terminan en sesión o compra. None si todavía no hay consultas."""
    consultas = total(registros, "consulta", origen)
    return total(registros, "agendo", origen) / consultas * 100 if consultas else None


def por_origen(registros: list[dict]) -> list[dict]:
    """Una fila por origen con sus cantidades por etapa y su conversión, de más a menos clientas."""
    origenes = sorted({r["origen"] for r in registros})
    filas = [{"origen": o, **{e: total(registros, e, o) for e in ETAPAS}, "conversion": conversion(registros, o)} for o in origenes]
    return sorted(filas, key=lambda f: (f["agendo"], f["consulta"]), reverse=True)
