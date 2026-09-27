"""Página principal: la conversación con Nexus, "Tu día con Nexus" y la memoria.

Responsable: Persona 1 (Interfaz).
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

from nexus import actividad, demo, estadisticas, inicio, memoria, revision
from nexus.config import config_ia
from nexus.prompts import MODOS

# Módulos cuyo resultado Bárbara publica o envía: ahí se revisa el texto antes de copiarlo.
MODOS_PARA_PUBLICAR = {"guion", "experiencia", "difusion"}

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


def texto_para_copiar(respuesta: str) -> str:
    """Quita el aviso del modo demo y las marcas de Markdown, que Instagram y WhatsApp no entienden."""
    texto = respuesta.split("\n\n---\n")[0]
    texto = re.sub(r"^(\s*)\* ", r"\1- ", texto, flags=re.MULTILINE)  # viñetas con * pasan a -
    texto = texto.replace("*", "").replace("__", "")  # negritas y cursivas
    texto = re.sub(r"^(#+|>)\s*", "", texto, flags=re.MULTILINE)  # títulos y citas
    return texto.strip()


def mostrar_revision(respuesta: str) -> None:
    """Avisa si el texto tiene promesas de salud, precios o datos por completar (ver nexus/revision.py)."""
    alertas = revision.revisar(texto_para_copiar(respuesta))
    if not alertas:
        st.caption("✅ Revisado: sin promesas de salud ni datos por completar. Igual léelo antes de publicar.")
        return
    # El $ se escapa porque Streamlit lo interpreta como fórmula matemática.
    lineas = "\n".join(f"- **“{a.frase.replace('$', chr(92) + '$')}”**: {a.consejo}" for a in alertas)
    if revision.hay_rojas(alertas):
        st.error(f"Antes de publicar o enviar, cambia esto:\n\n{lineas}", icon="✋")
    else:
        st.warning(f"Revisa esto antes de publicar o enviar:\n\n{lineas}", icon="👀")


def generar_respuesta(historial: list[dict], imagenes: list[tuple[bytes, str]]) -> str:
    if not api_key:
        return demo.responder(modo)
    from nexus.ia import IASaturada, responder

    try:
        return responder(modo, historial, memoria.como_texto(recuerdos), api_key, modelo, imagenes, base_url)
    except IASaturada:
        # Plan gratis de Gemini: 15 consultas por minuto por modelo. Se libera solo en un momento.
        return ("Uf, Bárbara, en este momento estoy recibiendo muchas consultas y necesito un respiro 🌿 "
                "Espera un minuto y vuelve a enviarme tu mensaje.")
    except Exception:
        return "No pude conectarme con la IA en este momento 🌿 Revisa tu internet y vuelve a intentarlo en un minuto."


def recordar(texto: str, respuesta: str) -> list[str]:
    """Actualiza los consolidados de la memoria con lo nuevo. Devuelve los temas que cambiaron."""
    if not api_key:
        # Modo demo: sin IA no se puede resumir, así que solo se guarda lo contado en "Conversemos".
        return memoria.agregar_sin_ia(recuerdos, texto, ahora.date()) if modo == "conversemos" else []
    from nexus.ia import actualizar_memoria

    material = f"Bárbara dijo: {texto}"
    if modo == "estadisticas":
        material += f"\n\nAnálisis de sus estadísticas:\n{respuesta}"
    try:
        cambios = actualizar_memoria(material, memoria.como_json(recuerdos), memoria.TEMAS, api_key, modelo, base_url)
    except Exception:
        return []  # si falla la memoria, la conversación sigue igual
    return memoria.actualizar(recuerdos, cambios, ahora.date())


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
            actualizados = recordar(texto, respuesta)
            numeros = guardar_numeros(imagenes, texto)
    historial.append({"role": "assistant", "content": respuesta})
    avisos = []
    if actualizados:
        avisos.append("Actualicé lo que sé de ti: " + ", ".join(f"{memoria.TEMAS[t][0]} {memoria.TEMAS[t][1]}" for t in actualizados))
    if numeros:
        avisos.append(f"Anoté los números de {numeros} {'publicación' if numeros == 1 else 'publicaciones'} en 📈 Tu alcance")
    if avisos:
        st.session_state.aviso = ". ".join(avisos)
    st.rerun()


def guardar_numeros(imagenes: list[tuple[bytes, str]], texto: str) -> int:
    """Si subió capturas, saca sus números para la página "Tu alcance". Devuelve cuántas publicaciones anotó."""
    if not imagenes or not api_key:
        return 0
    from nexus.ia import extraer_metricas

    try:
        filas = extraer_metricas(imagenes, texto, api_key, modelo, base_url)
    except Exception:
        return 0  # el análisis en texto ya se mostró; los números se pueden cargar a mano
    return estadisticas.agregar(estadisticas.cargar(), filas)


def preparar_inicio() -> dict:
    """Saludo y acciones del día. Se calcula una vez por visita para no llamar a la IA en cada clic."""
    dias = actividad.dias_sin_publicar(registro, ahora.date())
    if api_key:
        from nexus.ia import generar_inicio

        try:
            return generar_inicio(memoria.como_texto(recuerdos), inicio.contexto(recuerdos, dias, ahora), api_key, modelo, base_url)
        except Exception:
            pass  # si la IA falla, se usan las reglas
    return inicio.por_reglas(recuerdos, dias, ahora)


@st.dialog("Lo que Nexus sabe de ti", width="large")
def ver_tema(tema: str) -> None:
    """Ventana con un consolidado completo: Bárbara puede leerlo, corregirlo u olvidarlo."""
    emoji, titulo, _ = memoria.TEMAS[tema]
    consolidado = recuerdos[tema]
    st.subheader(f"{emoji} {titulo}")
    fecha = datetime.strptime(consolidado["actualizado"], "%Y-%m-%d").strftime("%d-%m-%Y") if consolidado["actualizado"] else ""
    st.caption(f"Actualizado el {fecha}. Si algo no es cierto, corrígelo aquí mismo.")
    nuevo = st.text_area(titulo, consolidado["texto"], height=260, label_visibility="collapsed")

    if st.session_state.get("olvidar_tema") == tema:
        st.warning("¿Quieres que olvide todo este tema? No se puede deshacer.")
        col_si, col_no = st.columns(2)
        if col_si.button("Sí, olvidar", type="primary", width="stretch"):
            memoria.olvidar(recuerdos, tema)
            del st.session_state.olvidar_tema
            st.rerun()
        if col_no.button("Cancelar", width="stretch"):
            del st.session_state.olvidar_tema
            st.rerun(scope="fragment")
    else:
        col_guardar, col_olvidar = st.columns(2)
        if col_guardar.button("Guardar cambios", icon=":material/check:", type="primary", width="stretch",
                              disabled=nuevo.strip() == consolidado["texto"]):
            memoria.actualizar(recuerdos, {tema: nuevo}, ahora.date())
            st.session_state.aviso = f"Listo, corregí {emoji} {titulo}"
            st.rerun()
        if col_olvidar.button("Olvidar este tema", icon=":material/delete:", width="stretch"):
            st.session_state.olvidar_tema = tema
            st.rerun(scope="fragment")


def elegir_accion(accion: dict) -> None:
    """Al pulsar una acción del día: abre su módulo y deja listo el primer mensaje."""
    st.session_state.modo = accion["modo"]
    st.session_state.pendiente = accion.get("mensaje")


api_key, base_url, modelo = config_ia()
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
    else:
        st.caption("Se va completando con cada conversación. Toca un tema para verlo entero o corregirlo.")
    for tema, (emoji, titulo, _) in memoria.TEMAS.items():
        if tema not in recuerdos:
            continue
        with st.container(border=True):
            if st.button(f"{emoji} {titulo}", key=f"tema-{tema}", type="tertiary"):
                ver_tema(tema)
            texto = recuerdos[tema]["texto"]
            st.caption(texto[:90] + ("…" if len(texto) > 90 else ""))

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
        if modo in MODOS_PARA_PUBLICAR:
            mostrar_revision(mensaje["content"])
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
