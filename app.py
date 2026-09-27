"""Interfaz de Nexus en Streamlit.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

from nexus import actividad, demo, inicio, memoria
from nexus.prompts import MODOS

st.set_page_config(page_title="Nexus · Terapias Dalmeet", page_icon="🌿", layout="centered")

# Frases de ejemplo para que Bárbara no parta frente a una caja vacía.
EJEMPLOS = {
    "conversemos": [
        "Siento que el cariño que pongo en lo que hago le llega a la otra persona",
        "Mi sueño es hacer giras de terapia por distintas ciudades",
        "En Brasil aprendí que el autocuidado es parte del día a día",
    ],
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


def generar_respuesta(historial: list[dict], imagenes: list[tuple[bytes, str]]) -> str:
    if not api_key:
        return demo.responder(modo)
    from nexus.ia import responder

    try:
        return responder(modo, historial, memoria.como_texto(recuerdos), api_key, modelo, imagenes)
    except Exception as error:
        st.warning(f"No pude conectarme con la IA ({error}). Te muestro un ejemplo.")
        return demo.responder(modo)


def recordar(texto: str, respuesta: str) -> int:
    """Guarda en la memoria lo nuevo que vale la pena recordar. Devuelve cuántos recuerdos se agregaron."""
    if not api_key:
        # Modo demo: sin IA no se puede resumir, así que solo se guarda lo contado en "Conversemos".
        return memoria.agregar(recuerdos, [texto], "esencia") if modo == "conversemos" else 0
    from nexus.ia import extraer_recuerdos

    material = f"Bárbara dijo: {texto}"
    if modo == "estadisticas":
        material += f"\n\nAnálisis de sus estadísticas:\n{respuesta}"
    try:
        nuevos = extraer_recuerdos(material, memoria.como_texto(recuerdos), api_key, modelo)
    except Exception:
        return 0  # si falla la memoria, la conversación sigue igual
    return sum(memoria.agregar(recuerdos, textos, tipo) for tipo, textos in nuevos.items())


def enviar(texto: str, archivos: list | None = None) -> None:
    imagenes = [(archivo.getvalue(), archivo.type) for archivo in archivos or []]
    if imagenes and not texto:
        texto = "Te comparto mis estadísticas."
    historial.append({"role": "user", "content": texto, "imagenes": [datos for datos, _ in imagenes]})
    with st.chat_message("user"):
        st.markdown(texto)
    with st.chat_message("assistant", avatar="🌿"):
        with st.spinner("Aterrizando tu idea..."):
            respuesta = generar_respuesta(historial, imagenes)
            agregados = recordar(texto, respuesta)
    historial.append({"role": "assistant", "content": respuesta})
    if agregados:
        st.session_state.aviso = f"Guardé {agregados} {'cosa nueva' if agregados == 1 else 'cosas nuevas'} sobre ti 💭"
    st.rerun()


def preparar_inicio() -> dict:
    """Saludo y acciones del día. Se calcula una vez por visita para no llamar a la IA en cada clic."""
    dias = actividad.dias_sin_publicar(registro, ahora.date())
    if api_key:
        from nexus.ia import generar_inicio

        try:
            return generar_inicio(memoria.como_texto(recuerdos), inicio.contexto(recuerdos, dias, ahora), api_key, modelo)
        except Exception:
            pass  # si la IA falla, se usan las reglas
    return inicio.por_reglas(recuerdos, dias, ahora)


def elegir_accion(accion: dict) -> None:
    """Al pulsar una acción del día: abre su módulo y deja listo el primer mensaje."""
    st.session_state.modo = accion["modo"]
    st.session_state.pendiente = accion.get("mensaje")


api_key = obtener_secreto("OPENAI_API_KEY")
modelo = obtener_secreto("OPENAI_MODEL") or "gpt-4o-mini"
ahora = datetime.now(ZoneInfo("America/Santiago"))  # hora de Chile, aunque el servidor esté en otro país
recuerdos = memoria.cargar()
registro = actividad.cargar()

# Una conversación separada por módulo, para no mezclar guiones con propuestas.
if "conversaciones" not in st.session_state:
    st.session_state.conversaciones = {m: [] for m in MODOS}
# Ideas marcadas con 💚. Se guardan aparte para no perderlas al empezar de nuevo.
if "guardadas" not in st.session_state:
    st.session_state.guardadas = []
guardadas = st.session_state.guardadas

if aviso := st.session_state.pop("aviso", None):
    st.toast(aviso, icon="🌿")

# --- Barra lateral: ideas que le sirvieron y memoria ---
with st.sidebar:
    st.metric("💚 Ideas que te sirvieron", len(guardadas))
    if guardadas:
        archivo = "\n\n".join(f"# {g['titulo']}\n\n{texto_para_copiar(g['contenido'])}" for g in guardadas)
        st.download_button("Descargar mis ideas", archivo, file_name="ideas_nexus.txt", icon="⬇️")
    else:
        st.caption("Marca con 💚 las respuestas que te sirvan y aquí podrás descargarlas.")

    st.divider()
    st.subheader("🧠 Lo que Nexus sabe de ti")
    if not recuerdos:
        st.caption("Aún nada. Cuéntame tus sueños en 💭 Conversemos o sube tus estadísticas.")
    for tipo, titulo in memoria.TIPOS.items():
        del_tipo = [(i, r) for i, r in enumerate(recuerdos) if r["tipo"] == tipo]
        if del_tipo:
            with st.expander(f"{titulo} ({len(del_tipo)})"):
                for i, recuerdo in del_tipo:
                    col_texto, col_borrar = st.columns([6, 1], vertical_alignment="center")
                    col_texto.markdown(recuerdo["texto"])
                    if col_borrar.button("🗑️", key=f"borrar-{i}", help="Olvidar esto"):
                        memoria.borrar(recuerdos, i)
                        st.rerun()

st.title("🌿 Nexus")
st.caption("Tu compañera para hacer crecer Terapias Dalmeet.")

if not api_key:
    st.info("Modo demo: sin API key, Nexus muestra respuestas de ejemplo.")

# --- Tu día con Nexus: solo al llegar, antes de empezar a conversar ---
if not any(st.session_state.conversaciones.values()):
    if "inicio" not in st.session_state:
        with st.spinner("Preparando tu día..."):
            st.session_state.inicio = preparar_inicio()
    with st.container(border=True):
        st.markdown(f"#### ☀️ Tu día con Nexus\n\n{st.session_state.inicio['saludo']}")
        st.caption("Para hoy te propongo:")
        for i, accion in enumerate(st.session_state.inicio["acciones"]):
            st.button(
                accion["titulo"],
                key=f"accion-{i}",
                icon=MODOS[accion["modo"]]["titulo"].split()[0],  # el emoji del módulo
                on_click=elegir_accion,
                args=(accion,),
                width="stretch",
            )

# --- Conversación ---
if "modo" not in st.session_state:
    st.session_state.modo = list(MODOS)[0]
modo = st.segmented_control(
    "¿En qué trabajamos hoy?",
    options=list(MODOS),
    format_func=lambda m: MODOS[m]["titulo"],
    key="modo",
    width="stretch",
)
modo = modo or list(MODOS)[0]  # si se deselecciona la opción activa
historial = st.session_state.conversaciones[modo]
acepta_imagenes = MODOS[modo].get("acepta_imagenes", False)

if pendiente := st.session_state.pop("pendiente", None):
    enviar(pendiente)  # viene de una acción de "Tu día con Nexus"

with st.chat_message("assistant", avatar="🌿"):
    st.markdown(MODOS[modo]["bienvenida"])

if not historial and EJEMPLOS.get(modo):
    st.caption("¿No sabes por dónde empezar? Prueba con una de estas:")
    for i, ejemplo in enumerate(EJEMPLOS[modo]):
        if st.button(ejemplo, key=f"ejemplo-{modo}-{i}", icon="💬"):
            enviar(ejemplo)

for i, mensaje in enumerate(historial):
    if mensaje["role"] == "user":
        with st.chat_message("user"):
            st.markdown(mensaje["content"])
            if mensaje.get("imagenes"):
                st.image(mensaje["imagenes"], width=160)
        continue

    with st.chat_message("assistant", avatar="🌿"):
        st.markdown(mensaje["content"])
        idea = {"titulo": MODOS[modo]["titulo"], "contenido": mensaje["content"]}
        util = idea in guardadas
        etiqueta = "Guardada en tus ideas" if util else "Me sirve"
        col_util, col_publicado = st.columns(2)
        if col_util.button(etiqueta, key=f"util-{modo}-{i}", icon="💚" if util else "🤍"):
            if util:
                guardadas.remove(idea)
            else:
                guardadas.append(idea)
            st.rerun()
        if modo == "guion" and col_publicado.button("Lo publiqué", key=f"publicado-{i}", icon="📣"):
            actividad.registrar_publicacion(registro, ahora.date())
            st.session_state.aviso = "¡Bien, Bárbara! Lo anoté. Cuando tengas estadísticas, súbelas en 📊 🌿"
            st.rerun()
        with st.expander("Copiar texto", icon="📋"):
            st.caption("Usa el ícono de copiar, arriba a la derecha del recuadro.")
            st.code(texto_para_copiar(mensaje["content"]), language=None, wrap_lines=True)

if historial and st.button("Empezar de nuevo", icon="🔄"):
    historial.clear()
    st.rerun()

# El cuadro va dentro de un contenedor (justo después de la conversación) y no fijo al pie:
# fijo, Streamlit "pega" la página al final y no deja subir bien con la rueda del mouse.
with st.container():
    entrada = st.chat_input(
        MODOS[modo]["placeholder"],
        accept_file="multiple" if acepta_imagenes else False,
        file_type=["png", "jpg", "jpeg", "webp"] if acepta_imagenes else None,
    )
if entrada:
    if acepta_imagenes:
        enviar(entrada.text, entrada.files)
    else:
        enviar(entrada)
