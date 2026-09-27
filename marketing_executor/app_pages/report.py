\
from __future__ import annotations

import streamlit as st

from dalmeet_executor.reporting import build_nexus_json, build_nexus_report
from dalmeet_executor.ui import campaign_selector, page_header

page_header(
    "Reporte para Nexus",
    "Cierra el ciclo: el Executor resume lo ocurrido y Nexus puede diseñar el siguiente plan.",
)

campaign = campaign_selector("report_campaign")
if not campaign:
    st.stop()

report = build_nexus_report(campaign.id)
json_report = build_nexus_json(campaign.id)

st.subheader("Texto listo para entregar a Nexus")
st.text_area(
    "Reporte",
    value=report,
    height=520,
    help="Selecciona y copia este contenido en Nexus.",
)

c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "Descargar reporte .txt",
        data=report.encode("utf-8"),
        file_name=f"reporte_nexus_campana_{campaign.id}.txt",
        mime="text/plain",
        use_container_width=True,
    )
with c2:
    st.download_button(
        "Descargar datos .json",
        data=json_report.encode("utf-8"),
        file_name=f"reporte_nexus_campana_{campaign.id}.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.subheader("Así funciona la retroalimentación")
st.markdown(
    """
1. Nexus crea el plan.
2. El Executor recibe y organiza las acciones.
3. Bárbara aprueba, modifica o rechaza.
4. El Executor ejecuta y registra resultados.
5. Este reporte vuelve a Nexus.
6. Nexus analiza el desempeño y genera el siguiente ciclo.
"""
)
