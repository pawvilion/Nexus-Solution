\
from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from dalmeet_executor.db import add_action, list_actions
from dalmeet_executor.ui import campaign_selector, page_header, status_badge

page_header(
    "Calendario",
    "Qué se hará, cuándo y en qué canal.",
)

campaign = campaign_selector("calendar_campaign")
if not campaign:
    st.stop()

actions = list_actions(campaign.id)

scheduled = []
unscheduled = []

for a in actions:
    row = {
        "Fecha": a.scheduled_for[:10] if a.scheduled_for else None,
        "Hora": a.scheduled_for[11:16] if a.scheduled_for and len(a.scheduled_for) >= 16 else "",
        "Acción": a.title,
        "Canal": a.channel,
        "Prioridad": a.priority,
        "Estado": status_badge(a.status),
    }
    (scheduled if a.scheduled_for else unscheduled).append(row)

if scheduled:
    df = pd.DataFrame(scheduled).sort_values(["Fecha", "Hora"])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No hay acciones programadas.")

if unscheduled:
    st.subheader("Sin fecha")
    st.dataframe(pd.DataFrame(unscheduled), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Agregar una acción manual")

with st.form("new_action", clear_on_submit=True):
    title = st.text_input("Título")
    c1, c2, c3 = st.columns(3)
    action_type = c1.selectbox(
        "Tipo",
        ["social_post", "story", "reel", "ad_campaign", "follow_up", "analysis", "email"],
    )
    channel = c2.selectbox(
        "Canal",
        ["instagram", "facebook", "whatsapp", "email", "internal"],
    )
    priority = c3.selectbox("Prioridad", ["baja", "media", "alta"], index=1)
    content = st.text_area("Contenido / instrucciones")
    c4, c5 = st.columns(2)
    date = c4.date_input("Fecha", value=None)
    time = c5.time_input("Hora", value=None)
    requires_approval = st.checkbox(
        "Requiere aprobación",
        value=True,
        help="Las acciones externas igual requerirán aprobación aunque se desmarque por error.",
    )
    submitted = st.form_submit_button("Agregar al calendario")

    if submitted:
        if not title.strip():
            st.error("Escribe un título.")
        else:
            scheduled_for = None
            if date:
                if time:
                    scheduled_for = f"{date.isoformat()}T{time.strftime('%H:%M:%S')}"
                else:
                    scheduled_for = f"{date.isoformat()}T09:00:00"

            # Regla de seguridad: todo canal externo requiere aprobación.
            if channel != "internal":
                requires_approval = True

            add_action(
                campaign_id=campaign.id,
                action_type=action_type,
                channel=channel,
                title=title.strip(),
                content=content,
                scheduled_for=scheduled_for,
                priority=priority,
                requires_approval=requires_approval,
            )
            st.success("Acción agregada.")
            st.rerun()
