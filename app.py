"""Punto de entrada de Bárbara.IA: decide qué página mostrar.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
Cada página está en la carpeta vistas/.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import streamlit as st

from nexus import semana

# ?p=tarjeta abre la tarjeta digital pública de Bárbara, sin menú ni nada de Bárbara.IA.
if st.query_params.get("p") == "tarjeta":
    st.set_page_config(page_title="Terapias Dalmeet", page_icon="🌿", layout="centered", initial_sidebar_state="collapsed")
    st.navigation([st.Page("vistas/tarjeta.py", title="Terapias Dalmeet")], position="hidden").run()
else:
    st.set_page_config(page_title="Bárbara.IA · Terapias Dalmeet", page_icon="🌿", layout="centered")
    # Su semana va en la barra lateral de todas las páginas, para que la vea siempre junto al chat.
    with st.sidebar:
        semana.mostrar_en_barra(datetime.now(ZoneInfo("America/Santiago")).weekday())
        st.divider()
    st.navigation(
        [
            st.Page("vistas/nexus.py", title="Bárbara.IA", icon="🌿", default=True),
            st.Page("vistas/kit.py", title="Kit de difusión", icon="📣", url_path="kit"),
            st.Page("vistas/alcance.py", title="Tu alcance", icon="📈", url_path="alcance"),
        ],
        position="top",
    ).run()
