"""Interfaz de Nexus en Streamlit.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
"""

import streamlit as st

from nexus.modelos import DIAS, PRIORIDADES, Preferencias, Tarea
from nexus import planificador_demo

st.set_page_config(page_title="Nexus · Tu semana ordenada", page_icon="🗓️", layout="wide")


def obtener_api_key() -> str | None:
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except FileNotFoundError:  # no existe .streamlit/secrets.toml
        return None


if "tareas" not in st.session_state:
    st.session_state.tareas = []

st.title("🗓️ Nexus")
st.caption("Escribe lo que tienes que hacer esta semana y Nexus te lo organiza.")

api_key = obtener_api_key()
if not api_key:
    st.info("Modo demo: no hay API key de OpenAI, se usa un planificador simple sin IA.")

# --- Barra lateral: preferencias ---
with st.sidebar:
    st.header("Preferencias")
    hora_inicio, hora_fin = st.slider("Horario", 0, 24, (9, 18))
    dias = st.multiselect("Días disponibles", DIAS, default=DIAS[:5])
    notas = st.text_area("Notas para la IA", placeholder="Ej.: prefiero hacer deporte por la mañana")

# --- Añadir tareas ---
with st.form("nueva_tarea", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    nombre = col1.text_input("Tarea")
    duracion = col2.number_input("Horas", min_value=0.25, max_value=12.0, value=1.0, step=0.25)
    prioridad = col3.selectbox("Prioridad", PRIORIDADES, index=1)
    dia_fijo = col4.selectbox("Día fijo", ["—"] + DIAS)
    if st.form_submit_button("Añadir") and nombre.strip():
        st.session_state.tareas.append(
            Tarea(nombre.strip(), duracion, prioridad, None if dia_fijo == "—" else dia_fijo)
        )

if st.session_state.tareas:
    st.subheader("Tareas")
    st.dataframe([t.to_dict() for t in st.session_state.tareas], width="stretch")
    if st.button("Borrar todas"):
        st.session_state.tareas = []
        st.rerun()

# --- Planificar ---
if st.button("✨ Organizar mi semana", type="primary", disabled=not st.session_state.tareas):
    preferencias = Preferencias(hora_inicio, hora_fin, tuple(dias), notas)
    tareas = st.session_state.tareas
    with st.spinner("Organizando tu semana..."):
        if api_key:
            from nexus.ia import MODELO_POR_DEFECTO, planificar_con_ia

            modelo = st.secrets.get("OPENAI_MODEL", MODELO_POR_DEFECTO)
            try:
                bloques = planificar_con_ia(tareas, preferencias, api_key, modelo)
            except Exception as error:
                st.warning(f"La IA falló ({error}). Uso el modo demo.")
                bloques = planificador_demo.planificar(tareas, preferencias)
        else:
            bloques = planificador_demo.planificar(tareas, preferencias)

    colocadas = {b.tarea for b in bloques}
    sin_hueco = [t.nombre for t in tareas if t.nombre not in colocadas]
    if sin_hueco:
        st.warning("No cupieron: " + ", ".join(sin_hueco))

    st.subheader("Tu semana")
    for dia, columna in zip(DIAS, st.columns(7)):
        with columna:
            st.markdown(f"**{dia}**")
            for b in sorted((b for b in bloques if b.dia == dia), key=lambda b: b.inicio):
                st.markdown(f"`{b.inicio}–{b.fin}`  \n{b.tarea}", help=b.motivo or None)
