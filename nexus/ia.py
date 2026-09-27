"""Integración con la API de OpenAI (ChatGPT).

Responsable: Persona 2 (IA).
Mientras no haya API key, la app responde con los ejemplos de nexus/demo.py.
"""

import base64
import json

from openai import OpenAI

from . import prompts

MODELO_POR_DEFECTO = "gpt-4o-mini"  # barato y entiende imágenes; se puede cambiar con MODELO en secrets

# Gemini (Google) tiene plan gratis y acepta el mismo formato que OpenAI: solo cambia la dirección y el modelo.
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODELO_POR_DEFECTO = "gemini-flash-lite-latest"  # rápido (2-3 s) y con plan gratis; gemini-2.5-flash ya no se ofrece a cuentas nuevas


def _leer_json(texto: str) -> dict:
    """Lee el JSON de la respuesta, aunque venga envuelto en ```json ... ``` (a Gemini le pasa)."""
    texto = texto.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    return json.loads(texto)


def responder(
    modo: str,
    historial: list[dict],
    memoria: str,
    api_key: str,
    modelo: str = MODELO_POR_DEFECTO,
    imagenes: list[tuple[bytes, str]] | None = None,
    base_url: str | None = None,
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

    cliente = OpenAI(api_key=api_key, base_url=base_url)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        temperature=0.8,  # algo de creatividad: es contenido, no cálculos
        messages=[{"role": "system", "content": prompts.sistema(modo, memoria)}, *mensajes],
    )
    return respuesta.choices[0].message.content


def generar_inicio(
    memoria: str, contexto: str, api_key: str, modelo: str = MODELO_POR_DEFECTO, base_url: str | None = None
) -> dict:
    """Saludo personal y 3 acciones para hoy: {"saludo": str, "acciones": [{"titulo", "modo", "mensaje"}]}."""
    cliente = OpenAI(api_key=api_key, base_url=base_url)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        temperature=0.9,  # que el saludo no sea igual todos los días
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": prompts.INICIO.format(
                modos=", ".join(prompts.MODOS), esencia=prompts.ESENCIA, memoria=memoria, contexto=contexto
            ),
        }],
    )
    datos = _leer_json(respuesta.choices[0].message.content)
    acciones = [a for a in datos.get("acciones", []) if a.get("modo") in prompts.MODOS][:3]
    if not datos.get("saludo") or not acciones:
        raise ValueError("La IA no devolvió un inicio válido")
    return {"saludo": datos["saludo"], "acciones": acciones}


def actualizar_memoria(
    texto: str,
    memoria_json: str,
    temas: dict,
    api_key: str,
    modelo: str = MODELO_POR_DEFECTO,
    base_url: str | None = None,
) -> dict:
    """Devuelve solo los temas que cambian, con su texto completo actualizado: {tema: texto}.

    memoria_json: textos actuales por tema (ver memoria.como_json).
    temas: {clave: (emoji, título, descripción)} (ver memoria.TEMAS).
    """
    lista_temas = "\n".join(f'- "{clave}": {descripcion}' for clave, (_, _, descripcion) in temas.items())
    cliente = OpenAI(api_key=api_key, base_url=base_url)
    respuesta = cliente.chat.completions.create(
        model=modelo,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompts.ACTUALIZAR_MEMORIA.format(temas=lista_temas, memoria=memoria_json)},
            {"role": "user", "content": texto},
        ],
    )
    datos = _leer_json(respuesta.choices[0].message.content)
    return {tema: texto for tema, texto in datos.items() if tema in temas and isinstance(texto, str)}
