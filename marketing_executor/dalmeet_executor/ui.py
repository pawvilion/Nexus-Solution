\
from __future__ import annotations

import streamlit as st

from .db import get_active_campaign, list_campaigns, set_active_campaign


def page_header(title: str, subtitle: str | None = None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)


def campaign_selector(key: str = "campaign_selector"):
    campaigns = list_campaigns()
    if not campaigns:
        st.info("Primero crea o importa una campaña en **Plan actual**.")
        return None

    active = get_active_campaign()
    options = {f"#{c.id} · {c.name}": c for c in campaigns}
    default_idx = 0
    if active:
        keys = list(options.keys())
        for i, key_name in enumerate(keys):
            if options[key_name].id == active.id:
                default_idx = i
                break

    chosen_label = st.selectbox(
        "Campaña",
        list(options.keys()),
        index=default_idx,
        key=key,
    )
    return options[chosen_label]


def status_badge(status: str) -> str:
    labels = {
        "propuesta": "Pendiente de aprobación",
        "aprobada": "Aprobada",
        "cambios_solicitados": "Cambios solicitados",
        "rechazada": "Rechazada",
        "ejecutada": "Ejecutada",
    }
    return labels.get(status, status)
