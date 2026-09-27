"""Números de las publicaciones de Bárbara, sacados de sus capturas de Instagram.

Responsable: Persona 3.
Se guardan en data/estadisticas.json (fuera de GitHub) para ver cómo evoluciona su alcance.
"""

import json
from pathlib import Path

ARCHIVO = Path(__file__).parent.parent / "data" / "estadisticas.json"

# Columnas de cada publicación: clave -> nombre que ve Bárbara.
METRICAS = {
    "alcance": "Cuentas alcanzadas",
    "me_gusta": "Me gusta",
    "comentarios": "Comentarios",
    "guardados": "Guardados",
    "compartidos": "Compartidos",
    "visitas_perfil": "Visitas al perfil",
    "seguidores_nuevos": "Seguidores nuevos",
}
COLUMNAS = {"publicacion": "Publicación", "fecha": "Fecha", "formato": "Formato"} | METRICAS
FORMATOS = ["Reel", "Carrusel", "Foto", "Historia", "Otro"]


def cargar() -> list[dict]:
    try:
        return json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar(publicaciones: list[dict]) -> None:
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(publicaciones, ensure_ascii=False, indent=2), encoding="utf-8")


def _limpiar(fila: dict) -> dict | None:
    """Deja solo las columnas conocidas, con números enteros. None si no tiene nombre ni alcance."""
    limpia = {"publicacion": str(fila.get("publicacion") or "").strip(), "fecha": str(fila.get("fecha") or "").strip()}
    formato = str(fila.get("formato") or "").strip().capitalize()
    limpia["formato"] = formato if formato in FORMATOS else "Otro"
    for clave in METRICAS:
        valor = fila.get(clave)
        try:
            if isinstance(valor, (int, float)):
                limpia[clave] = int(valor)
            else:  # texto como "1.240": en Chile el punto separa miles
                limpia[clave] = int(float(str(valor).replace(".", "").replace(",", ".")))
        except (TypeError, ValueError):
            limpia[clave] = None
    if not limpia["publicacion"] or limpia["alcance"] is None:
        return None
    return limpia


def agregar(publicaciones: list[dict], nuevas: list[dict]) -> int:
    """Agrega o actualiza publicaciones (misma publicación y fecha = la misma). Devuelve cuántas cambiaron."""
    cambios = 0
    for fila in filter(None, map(_limpiar, nuevas)):
        clave = (fila["publicacion"].lower(), fila["fecha"])
        existente = next((p for p in publicaciones if (p["publicacion"].lower(), p["fecha"]) == clave), None)
        if existente:
            existente.update({k: v for k, v in fila.items() if v is not None and k != "publicacion"})
        else:
            publicaciones.append(fila)
        cambios += 1
    if cambios:
        guardar(publicaciones)
    return cambios


def reemplazar(filas: list[dict]) -> list[dict]:
    """Guarda la tabla tal como la dejó Bárbara al editarla a mano."""
    publicaciones = list(filter(None, map(_limpiar, filas)))
    guardar(publicaciones)
    return publicaciones
