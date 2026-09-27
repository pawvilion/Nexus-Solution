\
import streamlit as st

from dalmeet_executor.db import init_db

st.set_page_config(
    page_title="Dalmeet Marketing Executor",
    page_icon="⚙️",
    layout="wide",
)

init_db()

pages = {
    "Marketing": [
        st.Page("app_pages/home.py", title="Inicio", icon=":material/home:", default=True),
        st.Page("app_pages/plan.py", title="Plan actual", icon=":material/strategy:"),
        st.Page("app_pages/approvals.py", title="Aprobaciones", icon=":material/approval:"),
        st.Page("app_pages/calendar.py", title="Calendario", icon=":material/calendar_month:"),
        st.Page("app_pages/results.py", title="Resultados", icon=":material/analytics:"),
        st.Page("app_pages/report.py", title="Reporte para Nexus", icon=":material/sync_alt:"),
    ]
}

pg = st.navigation(pages)

with st.sidebar:
    st.caption("DALMEET")
    st.markdown("**Marketing Executor**")
    st.caption("Nexus piensa · Bárbara aprueba · Executor ejecuta y mide")

pg.run()
