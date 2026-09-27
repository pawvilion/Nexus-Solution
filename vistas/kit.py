"""Kit de difusión: la tarjeta digital de Bárbara y afiches con QR para ferias, juntas de vecinos, etc.

Responsable: Persona 3.
"""

import re

import streamlit as st

from nexus import difusion, memoria
from nexus.config import config_ia, numero_whatsapp, url_app

api_key, base_url, modelo = config_ia()
numero = numero_whatsapp()

# Textos iniciales del afiche (Bárbara los cambia o le pide a Bárbara.IA que los sugiera).
for clave, valor in {
    "afiche_origen": "la feria de mi villa",
    "afiche_titulo": "Regálate una pausa",
    "afiche_subtitulo": "Terapias holísticas y guateros hechos a mano, con cariño",
    "afiche_detalle": "Masajes, reiki, reflexología y aromaterapia\nEn Puente Alto o a domicilio\nEscríbeme y conversamos qué necesitas",
}.items():
    st.session_state.setdefault(clave, valor)


def sugerir_textos() -> None:
    """Pide a la IA un texto pensado para el lugar donde irá el afiche (corre antes de dibujar la página)."""
    from nexus.ia import sugerir_afiche

    try:
        textos = sugerir_afiche(st.session_state.afiche_origen, memoria.como_texto(memoria.cargar()), api_key, modelo, base_url)
    except Exception:
        st.session_state.aviso_kit = "No pude conectarme con la IA. Prueba de nuevo en un minuto."
        return
    for campo in ("titulo", "subtitulo", "detalle"):
        if textos[campo]:
            st.session_state[f"afiche_{campo}"] = textos[campo]


st.title("📣 Kit de difusión")
st.caption("Para que te conozcan más allá de Instagram: tu tarjeta digital y afiches con QR para imprimir o compartir.")

if not numero:
    st.warning(
        "Falta tu número de WhatsApp. Pídele a tu equipo que lo agregue en los Secrets de la app "
        '(`WHATSAPP_NUMERO = "569..."`). Mientras tanto, los QR llevan a tu tarjeta digital.',
        icon="📱",
    )

# --- Tarjeta digital ---
with st.container(border=True):
    st.subheader("🌿 Tu tarjeta digital")
    st.write(
        "Una página con quién eres, tus terapias y tus productos, y un botón para escribirte por WhatsApp. "
        "Ponla en la bio de Instagram o compártela por WhatsApp."
    )
    link_bio = difusion.link_tarjeta(url_app(), "Instagram")
    st.code(link_bio, language=None)
    st.link_button("Ver cómo se ve", difusion.link_tarjeta(url_app(), None), icon="👀")

# --- Afiche con QR ---
st.subheader("🖨️ Crea un afiche con QR")
st.write(
    "Cada afiche lleva un QR que dice **dónde lo pusiste**. Cuando alguien te escriba, su mensaje dirá "
    "*\"te encontré por la feria de…\"*, así sabrás qué lugar te trae más clientas."
)

st.text_input("¿Dónde lo vas a usar?", key="afiche_origen", help="Ej.: la feria de la Villa Los Aromos, el CESFAM, la junta de vecinos de…")
if api_key:
    st.button("Que Bárbara.IA me sugiera el texto", icon="✨", on_click=sugerir_textos)
if aviso := st.session_state.pop("aviso_kit", None):
    st.warning(aviso)
st.text_input("Título", key="afiche_titulo")
st.text_input("Subtítulo", key="afiche_subtitulo")
st.text_area("Detalle (una idea por línea, máximo 4)", key="afiche_detalle", height=120)

destinos = ["WhatsApp directo", "Mi tarjeta digital"] if numero else ["Mi tarjeta digital"]
destino = st.radio(
    "¿Adónde lleva el QR?",
    destinos,
    horizontal=True,
    help="WhatsApp directo siempre funciona al instante. La tarjeta muestra más de ti, pero si nadie ha abierto "
    "la app en muchas horas puede tardar unos segundos en despertar.",
)
origen = st.session_state.afiche_origen.strip()
if destino == "WhatsApp directo":
    url_qr, texto_qr = difusion.link_whatsapp(numero, origen), "Escanéame y escríbeme por WhatsApp"
else:
    url_qr, texto_qr = difusion.link_tarjeta(url_app(), origen), "Escanéame para conocerme"

afiche = difusion.crear_afiche(
    st.session_state.afiche_titulo, st.session_state.afiche_subtitulo, st.session_state.afiche_detalle, url_qr, texto_qr
)
nombre_archivo = "afiche_" + (re.sub(r"[^a-z0-9]+", "_", origen.lower()).strip("_") or "dalmeet")

col_vista, col_descargas = st.columns([3, 2])
col_vista.image(afiche, caption="Vista previa", width="stretch")
with col_descargas:
    st.download_button("Descargar para imprimir (PDF)", difusion.como_pdf(afiche), f"{nombre_archivo}.pdf",
                       "application/pdf", icon="🖨️", width="stretch")
    st.download_button("Descargar imagen (PNG)", difusion.como_png(afiche), f"{nombre_archivo}.png",
                       "image/png", icon="🖼️", width="stretch")
    st.caption("La imagen sirve para Instagram (formato vertical) o para enviarla por WhatsApp.")
    st.caption(f"El QR lleva a: {url_qr}")
