"""Memoria de Nexus: lo que Bárbara va contando, ordenado en consolidados por tema.

Responsable: Persona 3.
Cada tema es un texto que la IA reescribe y enriquece con cada conversación.
Se guarda en data/memoria.json (fuera de GitHub, ver .gitignore).
Ojo: en Streamlit Cloud el disco se borra cuando la app se reinicia. Para una memoria
permanente hay que cambiar solo este archivo por una base de datos (ej. Supabase).
"""

import json
from datetime import date
from pathlib import Path

ARCHIVO = Path(__file__).parent.parent / "data" / "memoria.json"

# Temas de la memoria: clave -> (emoji, título que ve Bárbara, qué va en él).
TEMAS = {
    "suenos": ("🌟", "Tus sueños y metas", "lo que sueña y quiere lograr con su emprendimiento"),
    "creencias": ("💛", "Lo que crees y te mueve", "sus creencias, valores y lo que la motiva"),
    "historia": ("📖", "Tu historia", "anécdotas, experiencias y momentos importantes de su camino"),
    "trabajo": ("🌿", "Tu trabajo y tus clientas", "sus terapias, productos, forma de trabajar y a quién atiende"),
    "redes": ("📊", "Lo que funciona en tus redes", "qué formatos, temas y horarios le funcionan o no en redes"),
}


def cargar() -> dict:
    """Devuelve {tema: {"texto": str, "actualizado": "AAAA-MM-DD"}} solo con los temas que tienen algo."""
    try:
        datos = json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    if isinstance(datos, list):  # formato antiguo: lista de frases sueltas
        return _migrar(datos)
    return {tema: valor for tema, valor in datos.items() if tema in TEMAS}


def _migrar(recuerdos: list[dict]) -> dict:
    """Convierte la lista antigua de frases en consolidados, para no perder lo ya guardado."""
    memoria = {}
    for recuerdo in recuerdos:
        tema = "redes" if recuerdo.get("tipo") == "redes" else "creencias"
        anterior = memoria.get(tema, {}).get("texto", "")
        memoria[tema] = {"texto": f"{anterior}\n{recuerdo['texto']}".strip(), "actualizado": recuerdo.get("fecha", "")}
    guardar(memoria)
    return memoria


def guardar(memoria: dict) -> None:
    ARCHIVO.parent.mkdir(exist_ok=True)
    ARCHIVO.write_text(json.dumps(memoria, ensure_ascii=False, indent=2), encoding="utf-8")


def actualizar(memoria: dict, cambios: dict, hoy: date) -> list[str]:
    """Reemplaza el texto de los temas que cambiaron y guarda. Devuelve los temas actualizados."""
    actualizados = []
    for tema, texto in cambios.items():
        texto = (texto or "").strip()
        if tema in TEMAS and texto and texto != memoria.get(tema, {}).get("texto"):
            memoria[tema] = {"texto": texto, "actualizado": hoy.isoformat()}
            actualizados.append(tema)
    if actualizados:
        guardar(memoria)
    return actualizados


def agregar_sin_ia(memoria: dict, texto: str, hoy: date) -> list[str]:
    """Modo demo: sin IA no se puede resumir, así que se agrega lo contado tal cual."""
    anterior = memoria.get("creencias", {}).get("texto", "")
    return actualizar(memoria, {"creencias": f"{anterior}\n{texto}".strip()}, hoy)


def olvidar(memoria: dict, tema: str) -> None:
    memoria.pop(tema, None)
    guardar(memoria)


def como_json(memoria: dict) -> str:
    """Los textos actuales por tema, para que la IA los actualice."""
    return json.dumps({tema: memoria.get(tema, {}).get("texto", "") for tema in TEMAS}, ensure_ascii=False, indent=2)


def como_texto(memoria: dict) -> str:
    """Resumen de la memoria para incluirlo en el prompt de la IA."""
    if not memoria:
        return "Todavía no hay recuerdos guardados."
    return "\n\n".join(
        f"### {TEMAS[tema][1]}\n{memoria[tema]['texto']}" for tema in TEMAS if tema in memoria
    )
