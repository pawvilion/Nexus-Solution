"""Interfaz de Nexus en Streamlit.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
"""

import re

import streamlit as st

from nexus import demo
from nexus.prompts import MODOS

st.set_page_config(page_title="Nexus · Terapias Dalmeet", page_icon="🌿", layout="centered")

# Frases de ejemplo para que Bárbara no parta frente a una caja vacía.
EJEMPLOS = {
    "guion": [
        "Quiero contar que cada guatero lo hago a mano y con cariño",
        "Una clienta me dijo que durmió increíble después del masaje",
        "Quiero explicar por qué el estrés se nos acumula en la espalda",
    ],
    "experiencia": [
        "Quiero que la gente cree su propio guatero conmigo",
        "Me gustaría hacer una tarde de autocuidado para mamás",
        "Sueño con hacer giras de terapia por otras ciudades",
    ],
    "difusion": [
        "Quiero repetir la feria de mi villa en otra villa de Puente Alto",
        "Me gustaría ofrecer terapias express a los trabajadores de una empresa",
        "Quiero proponerle una actividad de bienestar a la municipalidad",
    ],
}


def obtener_secreto(nombre: str) -> str | None:
    try:
        return st.secrets.get(nombre)
    except FileNotFoundError:  # no existe .streamlit/secrets.toml
        return None


def texto_para_copiar(respuesta: str) -> str:
    """Quita el aviso del modo demo y las marcas de Markdown, que Instagram y WhatsApp no entienden."""
    texto = respuesta.split("\n\n---\n")[0]
    texto = re.sub(r"^(\s*)\* ", r"\1- ", texto, flags=re.MULTILINE)  # viñetas con * pasan a -
    texto = texto.replace("*", "").replace("__", "")  # negritas y cursivas
    texto = re.sub(r"^(#+|>)\s*", "", texto, flags=re.MULTILINE)  # títulos y citas
    return texto.strip()


def generar_respuesta(modo: str, historial: list[dict]) -> str:
    if not api_key:
        return demo.responder(modo)
    from nexus.ia import MODELO_POR_DEFECTO, responder

    try:
        return responder(modo, historial, api_key, obtener_secreto("OPENAI_MODEL") or MODELO_POR_DEFECTO)
    except Exception as error:
        st.warning(f"No pude conectarme con la IA ({error}). Te muestro un ejemplo.")
        return demo.responder(modo)


def enviar(texto: str) -> None:
    historial.append({"role": "user", "content": texto})
    with st.chat_message("user"):
        st.markdown(texto)
    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("Aterrizando tu idea..."):
            respuesta = generar_respuesta(modo, historial)
    historial.append({"role": "assistant", "content": respuesta})
    st.rerun()


api_key = obtener_secreto("OPENAI_API_KEY")

# Una conversación separada por módulo, para no mezclar guiones con propuestas.
if "conversaciones" not in st.session_state:
    st.session_state.conversaciones = {m: [] for m in MODOS}
# Ideas marcadas con 💚. Se guardan aparte para no perderlas al empezar de nuevo.
if "guardadas" not in st.session_state:
    st.session_state.guardadas = []
guardadas = st.session_state.guardadas

# --- Barra lateral: ideas que le sirvieron ---
with st.sidebar:
    st.metric("💚 Ideas que te sirvieron", len(guardadas))
    if guardadas:
        archivo = "\n\n".join(f"# {g['titulo']}\n\n{texto_para_copiar(g['contenido'])}" for g in guardadas)
        st.download_button("Descargar mis ideas", archivo, file_name="ideas_nexus.txt", icon="⬇️")
    else:
        st.caption("Marca con 💚 las respuestas que te sirvan y aquí podrás descargarlas.")

# --- Conversación ---
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

if not historial:
    st.caption("¿No sabes por dónde empezar? Prueba con una de estas:")
    for i, ejemplo in enumerate(EJEMPLOS[modo]):
        if st.button(ejemplo, key=f"ejemplo-{modo}-{i}", icon="💬"):
            enviar(ejemplo)

for i, mensaje in enumerate(historial):
    if mensaje["role"] == "user":
        with st.chat_message("user"):
            st.markdown(mensaje["content"])
        continue

    with st.chat_message("assistant", avatar="🌿"):
        st.markdown(mensaje["content"])
        idea = {"titulo": MODOS[modo]["titulo"], "contenido": mensaje["content"]}
        util = idea in guardadas
        etiqueta = "Guardada en tus ideas" if util else "Me sirve"
        if st.button(etiqueta, key=f"util-{modo}-{i}", icon="💚" if util else "🤍"):
            if util:
                guardadas.remove(idea)
            else:
                guardadas.append(idea)
            st.rerun()
        with st.expander("Copiar texto", icon="📋"):
            st.caption("Usa el ícono de copiar, arriba a la derecha del recuadro.")
            st.code(texto_para_copiar(mensaje["content"]), language=None, wrap_lines=True)

if historial and st.button("Empezar de nuevo", icon="🔄"):
    historial.clear()
    st.rerun()

if texto := st.chat_input(MODOS[modo]["placeholder"]):
    enviar(texto)
