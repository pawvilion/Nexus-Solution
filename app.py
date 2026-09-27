"""Punto de entrada de Nexus: decide qué página mostrar.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
Cada página está en la carpeta vistas/.
"""

import streamlit as st

# ?p=tarjeta abre la tarjeta digital pública de Bárbara, sin menú ni nada de Nexus.
if st.query_params.get("p") == "tarjeta":
    st.set_page_config(page_title="Terapias Dalmeet", page_icon="🌿", layout="centered", initial_sidebar_state="collapsed")
    st.navigation([st.Page("vistas/tarjeta.py", title="Terapias Dalmeet")], position="hidden").run()
else:
    st.set_page_config(page_title="Nexus · Terapias Dalmeet", page_icon="🌿", layout="centered")
    st.navigation(
        [
            st.Page("vistas/nexus.py", title="Nexus", icon="🌿", default=True),
            st.Page("vistas/kit.py", title="Kit de difusión", icon="📣", url_path="kit"),
            st.Page("vistas/alcance.py", title="Tu alcance", icon="📈", url_path="alcance"),
        ],
        position="top",
    ).run()
