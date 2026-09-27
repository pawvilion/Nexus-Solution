"""Integración con la API de OpenAI (ChatGPT).

Responsable: Persona 2 (IA).
Mientras no haya API key, la app responde con los ejemplos de nexus/demo.py.
"""

import base64
import json

from openai import InternalServerError, NotFoundError, OpenAI, RateLimitError

from . import prompts

MODELO_POR_DEFECTO = "gpt-4o-mini"  # barato y entiende imágenes; se puede cambiar con MODELO en secrets

# Gemini (Google) tiene plan gratis y acepta el mismo formato que OpenAI: solo cambia la dirección y el modelo.
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# Plan gratis: cada modelo tiene su propio cupo (Flash Lite: 15 consultas por minuto y 500 por día).
# Si el principal se satura, se usa el de respaldo, así la app aguanta el doble de uso.
GEMINI_MODELO_POR_DEFECTO = "gemini-3.5-flash-lite"  # rápido (2-3 s); gemini-2.5-flash ya no se ofrece a cuentas nuevas
GEMINI_RESPALDO = ["gemini-3.1-flash-lite"]


class IASaturada(Exception):
    """Se acabó el cupo gratis de todos los modelos por ahora (se libera en un minuto o al día siguiente)."""


def _completar(api_key: str, base_url: str | None, modelo: str, **opciones):
    """Llama al modelo y, si está saturado o no existe, prueba con los de respaldo (solo con Gemini)."""
    modelos = [modelo] + ([m for m in GEMINI_RESPALDO if m != modelo] if base_url == GEMINI_URL else [])
    # max_retries=0: si un modelo está saturado, es mejor pasar al siguiente que esperar y reintentar.
    cliente = OpenAI(api_key=api_key, base_url=base_url, max_retries=0 if len(modelos) > 1 else 2)
    for intento in modelos:
        try:
            return cliente.chat.completions.create(model=intento, **opciones)
        except (RateLimitError, NotFoundError, InternalServerError):
            continue  # saturado (429), dado de baja (404) o con alta demanda (503): probar el siguiente
    raise IASaturada("Todos los modelos de IA están ocupados en este momento")


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
        mensajes[-1]["content"] = _con_imagenes(mensajes[-1]["content"], imagenes)

    respuesta = _completar(
        api_key,
        base_url,
        modelo,
        temperature=0.8,  # algo de creatividad: es contenido, no cálculos
        messages=[{"role": "system", "content": prompts.sistema(modo, memoria)}, *mensajes],
    )
    return respuesta.choices[0].message.content


def generar_inicio(
    memoria: str, contexto: str, api_key: str, modelo: str = MODELO_POR_DEFECTO, base_url: str | None = None
) -> dict:
    """Saludo personal y 3 acciones para hoy: {"saludo": str, "acciones": [{"titulo", "modo", "mensaje"}]}."""
    respuesta = _completar(
        api_key,
        base_url,
        modelo,
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
    respuesta = _completar(
        api_key,
        base_url,
        modelo,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompts.ACTUALIZAR_MEMORIA.format(temas=lista_temas, memoria=memoria_json)},
            {"role": "user", "content": texto},
        ],
    )
    datos = _leer_json(respuesta.choices[0].message.content)
    return {tema: texto for tema, texto in datos.items() if tema in temas and isinstance(texto, str)}


def _con_imagenes(texto: str, imagenes: list[tuple[bytes, str]]) -> list[dict]:
    """Contenido de un mensaje con texto e imágenes, en el formato que entienden OpenAI y Gemini."""
    return [{"type": "text", "text": texto}] + [
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{base64.b64encode(datos).decode()}"}}
        for datos, mime in imagenes
    ]


def extraer_metricas(
    imagenes: list[tuple[bytes, str]], texto: str, api_key: str, modelo: str = MODELO_POR_DEFECTO, base_url: str | None = None
) -> list[dict]:
    """Lee las capturas de estadísticas y devuelve una fila por publicación con sus números."""
    respuesta = _completar(
        api_key,
        base_url,
        modelo,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompts.EXTRAER_METRICAS},
            {"role": "user", "content": _con_imagenes(f"Lo que dijo Bárbara: {texto}", imagenes)},
        ],
    )
    return _leer_json(respuesta.choices[0].message.content).get("publicaciones", [])


def sugerir_afiche(origen: str, memoria: str, api_key: str, modelo: str = MODELO_POR_DEFECTO, base_url: str | None = None) -> dict:
    """Propone título, subtítulo y detalle para un afiche pensado para un lugar concreto."""
    respuesta = _completar(
        api_key,
        base_url,
        modelo,
        temperature=0.8,
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": prompts.SUGERIR_AFICHE.format(origen=origen, esencia=prompts.ESENCIA, memoria=memoria)}],
    )
    datos = _leer_json(respuesta.choices[0].message.content)
    return {clave: str(datos.get(clave, "")).strip() for clave in ("titulo", "subtitulo", "detalle")}
