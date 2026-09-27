\
from __future__ import annotations

import json
import streamlit as st

from dalmeet_executor.brain_adapter import NEXUS_OUTPUT_INSTRUCTIONS, example_plan
from dalmeet_executor.db import (
    add_action,
    create_campaign,
    get_active_campaign,
    list_actions,
    list_campaigns,
    set_active_campaign,
)
from dalmeet_executor.import_plan import save_nexus_plan
from dalmeet_executor.ui import page_header

page_header(
    "Plan actual",
    "Nexus propone el plan. Este programa lo convierte en una campaña operativa independiente.",
)

tab_import, tab_manual, tab_current, tab_contract = st.tabs(
    ["Importar desde Nexus", "Crear manualmente", "Campañas", "Formato para Nexus"]
)

with tab_import:
    st.write(
        "Pega el JSON generado por Nexus. El Executor lo valida antes de crear cualquier acción."
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Cargar ejemplo", use_container_width=True):
            st.session_state["nexus_plan_input"] = json.dumps(
                example_plan(), ensure_ascii=False, indent=2
            )
    with c2:
        make_active = st.checkbox("Dejar esta campaña activa", value=True)

    raw = st.text_area(
        "Plan JSON",
        value=st.session_state.get("nexus_plan_input", ""),
        height=440,
        placeholder='{"campaign_name":"...", "objective":"...", "actions":[...]}',
    )

    if st.button("Validar e importar plan", type="primary"):
        try:
            campaign_id = save_nexus_plan(raw, make_active=make_active)
            st.success(f"Campaña #{campaign_id} creada correctamente.")
        except Exception as exc:
            st.error(str(exc))

with tab_manual:
    st.caption("Sirve para pruebas o para crear un plan sin Nexus.")
    with st.form("manual_campaign"):
        name = st.text_input("Nombre de la campaña")
        objective = st.text_area("Objetivo")
        c1, c2, c3 = st.columns(3)
        budget = c1.number_input("Presupuesto", min_value=0.0, step=10000.0)
        target_leads = c2.number_input("Meta de consultas", min_value=0, step=1)
        target_patients = c3.number_input("Meta de pacientes", min_value=0, step=1)
        c4, c5 = st.columns(2)
        start_date = c4.date_input("Inicio", value=None)
        end_date = c5.date_input("Término", value=None)
        active = st.checkbox("Activar inmediatamente", value=True)
        submitted = st.form_submit_button("Crear campaña")

        if submitted:
            if not name.strip() or not objective.strip():
                st.error("Completa nombre y objetivo.")
            else:
                row = create_campaign(
                    name=name.strip(),
                    objective=objective.strip(),
                    budget=budget,
                    target_leads=int(target_leads),
                    target_patients=int(target_patients),
                    start_date=start_date.isoformat() if start_date else None,
                    end_date=end_date.isoformat() if end_date else None,
                    make_active=active,
                )
                st.success(f"Campaña #{row.id} creada.")

with tab_current:
    campaigns = list_campaigns()
    if not campaigns:
        st.info("Aún no existen campañas.")
    else:
        active = get_active_campaign()
        for campaign in campaigns:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    active_text = " · ACTIVA" if active and campaign.id == active.id else ""
                    st.markdown(f"### {campaign.name}{active_text}")
                    st.write(campaign.objective)
                    st.caption(
                        f"Presupuesto: ${campaign.budget:,.0f} · "
                        f"Periodo: {campaign.start_date or '—'} → {campaign.end_date or '—'}"
                    )
                    st.write(f"Acciones: {len(list_actions(campaign.id))}")
                with c2:
                    if not (active and campaign.id == active.id):
                        if st.button(
                            "Activar",
                            key=f"activate_{campaign.id}",
                            use_container_width=True,
                        ):
                            set_active_campaign(campaign.id)
                            st.rerun()

with tab_contract:
    st.write(
        "Este texto es el contrato que deben agregar a Nexus cuando quieran que genere "
        "planes compatibles con el Executor."
    )
    st.code(NEXUS_OUTPUT_INSTRUCTIONS, language="text")
