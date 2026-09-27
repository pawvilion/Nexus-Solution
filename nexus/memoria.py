"""Memoria de Nexus: lo que Bárbara va contando y lo que se aprende de sus estadísticas.

Responsable: Persona 3.
Se guarda en data/memoria.json (fuera de GitHub, ver .gitignore).
Ojo: en Streamlit Cloud el disco se borra cuando la app se reinicia. Para una memoria
permanente hay que cambiar solo este archivo por una base de datos (ej. Supabase).
"""

import json
from datetime import date
from pathlib import Path

ARCHIVO = Path(__file__).parent.parent / "data" / "memoria.json"

# Tipos de recuerdo y cómo se muestran en la app.
TIPOS = {
    "esencia": "💭 Lo que eres y sueñas",
    "redes": "📊 Lo que funciona en tus redes",
}


def cargar() -> list[dict]:
    """Devuelve la lista de recuerdos: {"texto", "tipo", "fecha"}."""
    try:
        return json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar(recuerdos: list[dict]) -> None:
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(recuerdos, ensure_ascii=False, indent=2), encoding="utf-8")


def agregar(recuerdos: list[dict], textos: list[str], tipo: str) -> int:
    """Agrega los textos nuevos (sin repetir) y guarda. Devuelve cuántos se agregaron."""
    existentes = {r["texto"].strip().lower() for r in recuerdos}
    nuevos = [t.strip() for t in textos if t.strip() and t.strip().lower() not in existentes]
    recuerdos.extend({"texto": t, "tipo": tipo, "fecha": date.today().isoformat()} for t in nuevos)
    if nuevos:
        guardar(recuerdos)
    return len(nuevos)


def borrar(recuerdos: list[dict], indice: int) -> None:
    recuerdos.pop(indice)
    guardar(recuerdos)


def como_texto(recuerdos: list[dict]) -> str:
    """Resumen de la memoria para incluirlo en el prompt de la IA."""
    if not recuerdos:
        return "Todavía no hay recuerdos guardados."
    return "\n\n".join(
        f"### {titulo}\n" + "\n".join(f"- {r['texto']}" for r in recuerdos if r["tipo"] == tipo)
        for tipo, titulo in TIPOS.items()
        if any(r["tipo"] == tipo for r in recuerdos)
    )
