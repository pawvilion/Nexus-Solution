"""Configuración compartida por todas las páginas: claves, modelo de IA y datos de contacto.

Todo se lee de los Secrets de Streamlit (.streamlit/secrets.toml en local), nunca del código.
"""

import re

import streamlit as st

from .ia import GEMINI_MODELO_POR_DEFECTO, GEMINI_URL, MODELO_POR_DEFECTO

URL_APP_POR_DEFECTO = "https://nexus-dalmeet.streamlit.app"


def secreto(nombre: str) -> str | None:
    try:
        return st.secrets.get(nombre)
    except FileNotFoundError:  # no existe .streamlit/secrets.toml
        return None


def config_ia() -> tuple[str | None, str | None, str]:
    """(api_key, base_url, modelo). Sirve una clave de Gemini (gratis) o de OpenAI (de pago)."""
    if secreto("GEMINI_API_KEY"):
        api_key, base_url, modelo = secreto("GEMINI_API_KEY"), GEMINI_URL, GEMINI_MODELO_POR_DEFECTO
    else:
        api_key, base_url, modelo = secreto("OPENAI_API_KEY"), None, MODELO_POR_DEFECTO
    return api_key, base_url, secreto("MODELO") or modelo


def numero_whatsapp() -> str | None:
    """Número de WhatsApp de Bárbara solo con dígitos (ej. 56912345678), o None si no está configurado."""
    numero = re.sub(r"\D", "", secreto("WHATSAPP_NUMERO") or "")
    return numero or None


def url_app() -> str:
    return (secreto("APP_URL") or URL_APP_POR_DEFECTO).rstrip("/")
