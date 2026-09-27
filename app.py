"""Punto de entrada de Bárbara.IA: decide qué página mostrar.

Responsable: Persona 1 (Interfaz).
Ejecutar en local con:  streamlit run app.py
Cada página está en la carpeta vistas/.
"""

import streamlit as st

# Ajustes para el celular. En pantallas angostas Streamlit esconde el menú de arriba tras el ícono »,
# así que mostramos una fila de accesos directos (.st-key-menu_movil), y achicamos los títulos.
ESTILO_MOVIL = """
<style>
.st-key-menu_movil { display: none; }
@media (max-width: 640px) {
    .st-key-menu_movil { display: flex; margin-bottom: 0.5rem; }
    .st-key-menu_movil a { padding: 0.15rem 0.5rem; }
    h1 { font-size: 2rem !important; }
    h2 { font-size: 1.5rem !important; }
    h3 { font-size: 1.25rem !important; }
    h4 { font-size: 1.1rem !important; }
}
</style>
"""

# ?p=tarjeta abre la tarjeta digital pública de Bárbara, sin menú ni nada de Bárbara.IA.
if st.query_params.get("p") == "tarjeta":
    st.set_page_config(page_title="Terapias Dalmeet", page_icon="🌿", layout="centered", initial_sidebar_state="collapsed")
    st.html(ESTILO_MOVIL)
    st.navigation([st.Page("vistas/tarjeta.py", title="Terapias Dalmeet")], position="hidden").run()
else:
    st.set_page_config(page_title="Bárbara.IA · Terapias Dalmeet", page_icon="🌿", layout="centered")
    paginas = [
        st.Page("vistas/nexus.py", title="Bárbara.IA", icon="🌿", default=True),
        # Ciclo de marketing de Benjamín (paquete dalmeet_executor): plan de la IA → aprobación → ejecución → resultados → reporte.
        st.Page("vistas/executor.py", title="Marketing Executor", icon="⚙️", url_path="executor"),
        # Centro de marketing de Sofía (fotos editadas + descripción): oculto porque el equipo eligió el Executor.
        # st.Page("vistas/marketing.py", title="Centro de marketing", icon="📸", url_path="marketing"),
        st.Page("vistas/calendario.py", title="Calendario", icon="🗓️", url_path="calendario"),
        st.Page("vistas/kit.py", title="Kit de difusión", icon="📣", url_path="kit"),
        st.Page("vistas/alcance.py", title="Tu alcance", icon="📈", url_path="alcance"),
    ]
    pagina = st.navigation(paginas, position="top")

    st.html(ESTILO_MOVIL)
    # Menú del celular: nombres cortos para que quepan en una o dos filas.
    nombres_cortos = ["Inicio", "Marketing", "Semana", "Difusión", "Alcance"]
    with st.container(horizontal=True, gap="small", key="menu_movil"):
        for p, nombre in zip(paginas, nombres_cortos):
            st.page_link(p, label=nombre, icon=p.icon, width="content")

    pagina.run()
