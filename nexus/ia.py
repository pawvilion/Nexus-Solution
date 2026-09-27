"""Integración con la API de OpenAI (ChatGPT).

Responsable: Persona 2 (IA).
Mientras no haya API key, la app responde con los ejemplos de nexus/demo.py.
"""

import base64
import json

from openai import OpenAI

from . import prompts

MODELO_POR_DEFECTO = "gpt-4o-mini"  # barato y entiende imágenes; se puede cambiar con OPENAI_MODEL en secrets


def responder(
    modo: str,
    historial: list[dict],
    memoria: str,
    api_key: str,
    modelo: str = MODELO_POR_DEFECTO,
    imagenes: list[tuple[bytes, str]] | None = None,
) -> str:
    """Envía la conversación del módulo a ChatGPT y devuelve su respuesta en Markdown.

    historial: lista de {"role": "user" | "assistant", "content": str}, en orden.
    memoria: lo que Nexus recuerda de Bárbara (ver nexus/memoria.py).
    imagenes: capturas adjuntas al último mensaje, como (contenido, tipo MIME).
    """
    mensajes = [{"role": m["role"], "content": m["content"]} for m in historial]
    if imagenes:
        # Solo el último mensaje lleva las imágenes; el historial guarda únicamente el texto.
        mensajes[-1]["content"] = [{"type": "text", "text": mensajes[-1]["content"]}] + [
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(datos).decode()}"}}
            for datos, mime in imagenes
        ]

    cliente = OpenAI(api_key=api_key)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        temperature=0.8,  # algo de creatividad: es contenido, no cálculos
        messages=[{"role": "system", "content": prompts.sistema(modo, memoria)}, *mensajes],
    )
    return respuesta.choices[0].message.content


def extraer_recuerdos(texto: str, memoria: str, api_key: str, modelo: str = MODELO_POR_DEFECTO) -> dict:
    """Devuelve lo nuevo que vale la pena recordar: {"esencia": [...], "redes": [...]}."""
    cliente = OpenAI(api_key=api_key)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompts.EXTRAER_RECUERDOS.format(memoria=memoria)},
            {"role": "user", "content": texto},
        ],
    )
    datos = json.loads(respuesta.choices[0].message.content)
    return {"esencia": datos.get("esencia", []), "redes": datos.get("redes", [])}
