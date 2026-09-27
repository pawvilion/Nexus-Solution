\
from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from dalmeet_executor.db import (
    add_lead_event,
    add_metric,
    lead_total,
    list_actions,
    list_lead_events,
    list_metrics,
    metric_total,
)
from dalmeet_executor.ui import campaign_selector, page_header

page_header(
    "Resultados",
    "Registrar resultados sin guardar datos personales ni información clínica.",
)

campaign = campaign_selector("results_campaign")
if not campaign:
    st.stop()

consultations = lead_total(campaign.id, "consulta")
appointments = lead_total(campaign.id, "agendado")
patients = lead_total(campaign.id, "paciente")
spend = metric_total(campaign.id, "gasto")
reach = metric_total(campaign.id, "alcance")

conversion = (patients / consultations * 100) if consultations else 0
cac = (spend / patients) if patients else None

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Alcance", f"{reach:,.0f}")
c2.metric("Consultas", consultations)
c3.metric("Agendados", appointments)
c4.metric("Pacientes", patients)
c5.metric("Conversión", f"{conversion:.1f}%")

if cac is not None:
    st.caption(f"CAC estimado: ${cac:,.0f}".replace(",", "."))

tab_metrics, tab_leads, tab_history = st.tabs(
    ["Métricas de campañas", "Embudo anónimo", "Historial"]
)

with tab_metrics:
    actions = list_actions(campaign.id)
    action_options = {"General / campaña": None}
    action_options.update({f"#{a.id} · {a.title}": a.id for a in actions})

    with st.form("metric_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        chosen = c1.selectbox("Acción", list(action_options.keys()))
        metric_name = c2.selectbox(
            "Métrica",
            ["alcance", "impresiones", "clics", "interacciones", "gasto"],
        )
        c3, c4 = st.columns(2)
        metric_value = c3.number_input("Valor", min_value=0.0, step=1.0)
        metric_date = c4.date_input("Fecha", value=date.today())
        submitted = st.form_submit_button("Guardar métrica")

        if submitted:
            add_metric(
                campaign_id=campaign.id,
                action_id=action_options[chosen],
                metric_name=metric_name,
                metric_value=metric_value,
                recorded_date=metric_date.isoformat(),
            )
            st.success("Métrica guardada.")

with tab_leads:
    st.info(
        "Registra cantidades agregadas. No escribas nombres, teléfonos, RUT, diagnósticos "
        "ni otros datos de pacientes."
    )
    with st.form("lead_event_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        source = c1.selectbox(
            "Origen",
            ["Instagram", "Facebook", "WhatsApp", "Google", "Recomendación", "Otro"],
        )
        service = c2.selectbox(
            "Categoría de servicio",
            ["Terapia ocupacional", "Fonoaudiología", "Psicología", "Otro / general"],
        )
        c3, c4, c5 = st.columns(3)
        outcome = c3.selectbox("Resultado", ["consulta", "agendado", "paciente", "no_convirtió"])
        quantity = c4.number_input("Cantidad", min_value=1, step=1)
        event_date = c5.date_input("Fecha", value=date.today())
        submitted = st.form_submit_button("Registrar")

        if submitted:
            add_lead_event(
                campaign_id=campaign.id,
                source=source,
                service_category=service,
                outcome=outcome,
                quantity=int(quantity),
                recorded_date=event_date.isoformat(),
            )
            st.success("Resultado agregado.")

with tab_history:
    metrics = list_metrics(campaign.id)
    leads = list_lead_events(campaign.id)

    st.subheader("Métricas")
    if metrics:
        metrics_df = pd.DataFrame(
            [
                {
                    "Fecha": m.recorded_date,
                    "Métrica": m.metric_name,
                    "Valor": m.metric_value,
                    "Acción ID": m.action_id or "General",
                }
                for m in metrics
            ]
        )
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    else:
        st.caption("Sin métricas.")

    st.subheader("Embudo")
    if leads:
        lead_df = pd.DataFrame(
            [
                {
                    "Fecha": x.recorded_date,
                    "Origen": x.source,
                    "Servicio": x.service_category,
                    "Resultado": x.outcome,
                    "Cantidad": x.quantity,
                }
                for x in leads
            ]
        )
        st.dataframe(lead_df, use_container_width=True, hide_index=True)

        pivot = (
            lead_df.groupby(["Origen", "Resultado"])["Cantidad"]
            .sum()
            .unstack(fill_value=0)
        )
        st.bar_chart(pivot)
    else:
        st.caption("Sin datos de embudo.")
