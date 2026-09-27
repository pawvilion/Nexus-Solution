\
from __future__ import annotations

import pandas as pd
import streamlit as st

from dalmeet_executor.db import (
    get_active_campaign,
    lead_total,
    list_actions,
    metric_total,
)
from dalmeet_executor.ui import page_header

page_header(
    "Inicio",
    "Vista de supervisión para Bárbara: qué está pasando, qué necesita permiso y cómo va el objetivo.",
)

campaign = get_active_campaign()

if not campaign:
    st.warning("No hay una campaña activa.")
    st.page_link("app_pages/plan.py", label="Crear o importar el primer plan", icon=":material/add:")
    st.stop()

actions = list_actions(campaign.id)
pending = [a for a in actions if a.status == "propuesta"]
executed = [a for a in actions if a.status == "ejecutada"]
changes = [a for a in actions if a.status == "cambios_solicitados"]

consultations = lead_total(campaign.id, "consulta")
patients = lead_total(campaign.id, "paciente")
spend = metric_total(campaign.id, "gasto")

st.subheader(campaign.name)
st.write(campaign.objective)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Consultas", f"{consultations} / {campaign.target_leads or '—'}")
c2.metric("Nuevos pacientes", f"{patients} / {campaign.target_patients or '—'}")
c3.metric("Gasto", f"${spend:,.0f}".replace(",", "."))
c4.metric("Por aprobar", len(pending))

if campaign.budget:
    progress = min(spend / campaign.budget, 1.0)
    st.progress(progress, text=f"Presupuesto utilizado: {progress*100:.1f}%")

if campaign.target_patients:
    progress_patients = min(patients / campaign.target_patients, 1.0)
    st.progress(progress_patients, text=f"Meta de pacientes: {progress_patients*100:.1f}%")

st.divider()

left, right = st.columns([1.25, 1])

with left:
    st.subheader("Necesita tu atención")
    if pending:
        for action in pending[:5]:
            with st.container(border=True):
                st.markdown(f"**{action.title}**")
                st.caption(
                    f"{action.channel} · {action.priority} · "
                    f"{action.scheduled_for or 'sin fecha'}"
                )
        st.page_link(
            "app_pages/approvals.py",
            label=f"Revisar {len(pending)} acción(es)",
            icon=":material/approval:",
        )
    else:
        st.success("No hay acciones pendientes de aprobación.")

    if changes:
        st.info(f"{len(changes)} acción(es) tienen cambios solicitados.")

with right:
    st.subheader("Estado operativo")
    total = len(actions)
    if total:
        df = pd.DataFrame(
            {
                "Estado": ["Ejecutadas", "Pendientes", "Cambios solicitados", "Otras"],
                "Acciones": [
                    len(executed),
                    len(pending),
                    len(changes),
                    total - len(executed) - len(pending) - len(changes),
                ],
            }
        ).set_index("Estado")
        st.bar_chart(df)
    else:
        st.info("La campaña todavía no tiene acciones.")
