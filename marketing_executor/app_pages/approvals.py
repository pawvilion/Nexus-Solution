\
from __future__ import annotations

import streamlit as st

from dalmeet_executor.db import list_actions, update_action
from dalmeet_executor.executor import (
    approve_action,
    execute_action,
    reject_action,
    request_changes,
)
from dalmeet_executor.ui import campaign_selector, page_header, status_badge

page_header(
    "Aprobaciones",
    "Nada externo se ejecuta sin aprobación. Bárbara conserva el control final.",
)

campaign = campaign_selector("approval_campaign")
if not campaign:
    st.stop()

actions = list_actions(campaign.id)

filters = st.multiselect(
    "Mostrar estados",
    ["propuesta", "aprobada", "cambios_solicitados", "rechazada", "ejecutada"],
    default=["propuesta", "aprobada", "cambios_solicitados"],
)

visible = [a for a in actions if a.status in filters]

if not visible:
    st.info("No hay acciones con los filtros seleccionados.")
    st.stop()

for action in visible:
    with st.expander(
        f"{status_badge(action.status)} · {action.title}",
        expanded=action.status == "propuesta",
    ):
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Canal:** {action.channel}")
        c2.write(f"**Tipo:** {action.action_type}")
        c3.write(f"**Prioridad:** {action.priority}")

        st.caption(f"Programación: {action.scheduled_for or 'Sin fecha definida'}")

        edited_title = st.text_input(
            "Título",
            value=action.title,
            key=f"title_{action.id}",
        )
        edited_content = st.text_area(
            "Contenido / instrucciones",
            value=action.content,
            height=150,
            key=f"content_{action.id}",
        )
        review_note = st.text_area(
            "Nota de Bárbara",
            value=action.reviewer_note or "",
            placeholder="Ej.: cambiar el tono, eliminar una frase, revisar el CTA...",
            key=f"note_{action.id}",
        )

        b1, b2, b3, b4 = st.columns(4)

        if b1.button("Guardar cambios", key=f"save_{action.id}", use_container_width=True):
            update_action(
                action.id,
                title=edited_title.strip(),
                content=edited_content,
                reviewer_note=review_note,
            )
            st.success("Cambios guardados.")
            st.rerun()

        if b2.button("Aprobar", key=f"approve_{action.id}", use_container_width=True):
            try:
                update_action(action.id, title=edited_title.strip(), content=edited_content)
                approve_action(action.id, review_note)
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        if b3.button("Pedir cambios", key=f"changes_{action.id}", use_container_width=True):
            try:
                request_changes(action.id, review_note)
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        if b4.button("Rechazar", key=f"reject_{action.id}", use_container_width=True):
            try:
                reject_action(action.id, review_note)
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

        can_execute = (
            action.status == "aprobada"
            or (not action.requires_approval and action.channel == "internal")
        )
        if action.status != "ejecutada":
            if st.button(
                "Ejecutar ahora (simulación)",
                key=f"execute_{action.id}",
                type="primary",
                disabled=not can_execute,
            ):
                try:
                    result = execute_action(action.id, dry_run=True)
                    st.success(result)
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))

        if action.execution_result:
            st.info(action.execution_result)
