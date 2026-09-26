"""Integración con la API de OpenAI (ChatGPT).

Responsable: Persona 2 (IA).
Mientras no haya API key, la app usa nexus/planificador_demo.py automáticamente.
"""

import json

from openai import OpenAI

from . import prompts
from .modelos import Bloque, Preferencias, Tarea

MODELO_POR_DEFECTO = "gpt-4o-mini"  # barato; se puede cambiar con OPENAI_MODEL en secrets


def planificar_con_ia(
    tareas: list[Tarea],
    preferencias: Preferencias,
    api_key: str,
    modelo: str = MODELO_POR_DEFECTO,
) -> list[Bloque]:
    """Pide a ChatGPT el horario semanal y lo convierte en una lista de Bloques."""
    cliente = OpenAI(api_key=api_key)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompts.SISTEMA},
            {
                "role": "user",
                "content": prompts.mensaje_usuario(
                    json.dumps([t.to_dict() for t in tareas], ensure_ascii=False),
                    json.dumps(preferencias.to_dict(), ensure_ascii=False),
                ),
            },
        ],
    )
    datos = json.loads(respuesta.choices[0].message.content)
    return [Bloque(**b) for b in datos.get("bloques", [])]
