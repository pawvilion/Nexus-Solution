"""Interfaz de Nexus en Streamlit.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
"""

import streamlit as st

from nexus import demo
from nexus.prompts import MODOS

st.set_page_config(page_title="Nexus · Terapias Dalmeet", page_icon="🌿", layout="centered")


def obtener_secreto(nombre: str) -> str | None:
    try:
        return st.secrets.get(nombre)
    except FileNotFoundError:  # no existe .streamlit/secrets.toml
        return None


api_key = obtener_secreto("OPENAI_API_KEY")

# Una conversación separada por módulo, para no mezclar guiones con propuestas.
if "conversaciones" not in st.session_state:
    st.session_state.conversaciones = {modo: [] for modo in MODOS}

st.title("🌿 Hola, Bárbara")
st.caption("Cuéntame lo que sueñas para Terapias Dalmeet y lo convertimos en algo que puedas usar hoy.")

if not api_key:
    st.info("Modo demo: sin API key, Nexus muestra respuestas de ejemplo.")

modo = st.segmented_control(
    "¿En qué trabajamos hoy?",
    options=list(MODOS),
    format_func=lambda m: MODOS[m]["titulo"],
    default="guion",
    width="stretch",
)
modo = modo or "guion"  # si se deselecciona la opción activa
historial = st.session_state.conversaciones[modo]

with st.chat_message("assistant", avatar="🌿"):
    st.markdown(MODOS[modo]["bienvenida"])

for mensaje in historial:
    with st.chat_message(mensaje["role"], avatar="🌿" if mensaje["role"] == "assistant" else None):
        st.markdown(mensaje["content"])

if historial and st.button("Empezar de nuevo", icon="🔄"):
    historial.clear()
    st.rerun()

if texto := st.chat_input(MODOS[modo]["placeholder"]):
    historial.append({"role": "user", "content": texto})
    with st.chat_message("user"):
        st.markdown(texto)

    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("Aterrizando tu idea..."):
            if api_key:
                from nexus.ia import MODELO_POR_DEFECTO, responder

                try:
                    respuesta = responder(
                        modo, historial, api_key, obtener_secreto("OPENAI_MODEL") or MODELO_POR_DEFECTO
                    )
                except Exception as error:
                    st.warning(f"No pude conectarme con la IA ({error}). Te muestro un ejemplo.")
                    respuesta = demo.responder(modo)
            else:
                respuesta = demo.responder(modo)
        st.markdown(respuesta)
    historial.append({"role": "assistant", "content": respuesta})
    st.rerun()  # redibuja para que aparezca el botón "Empezar de nuevo"
