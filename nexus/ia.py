"""Integración con la API de OpenAI (ChatGPT).

Responsable: Persona 2 (IA).
Mientras no haya API key, la app responde con los ejemplos de nexus/demo.py.
"""

from openai import OpenAI

from . import prompts

MODELO_POR_DEFECTO = "gpt-4o-mini"  # barato; se puede cambiar con OPENAI_MODEL en secrets


def responder(modo: str, historial: list[dict], api_key: str, modelo: str = MODELO_POR_DEFECTO) -> str:
    """Envía la conversación del módulo a ChatGPT y devuelve su respuesta en Markdown.

    historial: lista de {"role": "user" | "assistant", "content": str}, en orden.
    """
    cliente = OpenAI(api_key=api_key)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        temperature=0.8,  # algo de creatividad: es contenido, no cálculos
        messages=[{"role": "system", "content": prompts.sistema(modo)}, *historial],
    )
    return respuesta.choices[0].message.content
