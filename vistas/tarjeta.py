"""Tarjeta digital pública de Terapias Dalmeet (lo que ven las futuras clientas).

Responsable: Persona 3.
Se abre con ?p=tarjeta (y ?origen=... para saber de dónde llegó la persona). No muestra nada de Bárbara.IA.
"""

import streamlit as st

from nexus import actividad
from nexus.config import numero_whatsapp
from nexus.difusion import TARJETA, link_whatsapp

origen = st.query_params.get("origen")

# Cuenta la visita una sola vez por persona, no en cada clic.
if not st.session_state.get("visita_contada"):
    actividad.registrar_visita(actividad.cargar(), origen)
    st.session_state.visita_contada = True

st.title(f"🌿 {TARJETA['nombre']}")
st.markdown(f"#### {TARJETA['lema']}")
st.caption(f"📍 {TARJETA['zona']}")

numero = numero_whatsapp()
if numero:
    st.link_button("Escríbeme por WhatsApp", link_whatsapp(numero, origen), type="primary", icon="💬", width="stretch")

st.write(TARJETA["sobre_mi"])

col_terapias, col_productos = st.columns(2)
with col_terapias.container(border=True):
    st.markdown("**Terapias**")
    st.markdown("\n".join(f"- {t}" for t in TARJETA["terapias"]))
with col_productos.container(border=True):
    st.markdown("**Hecho a mano**")
    st.markdown("\n".join(f"- {p}" for p in TARJETA["productos"]))

st.write(TARJETA["cierre"])
if numero:
    st.link_button("Conversemos por WhatsApp", link_whatsapp(numero, origen), icon="💬", width="stretch")
else:
    st.info("Muy pronto podrás escribirme por WhatsApp desde aquí.")
