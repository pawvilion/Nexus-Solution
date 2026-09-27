from __future__ import annotations

from .db import get_action, set_action_status


SAFE_AUTO_ACTIONS = {"analysis"}
EXTERNAL_CHANNELS = {"instagram", "facebook", "whatsapp", "email"}


def approve_action(action_id: int, reviewer_note: str | None = None) -> None:
    action = get_action(action_id)
    if not action:
        raise ValueError("Acción inexistente.")
    if action.status == "ejecutada":
        raise ValueError("La acción ya fue ejecutada.")
    set_action_status(action_id, "aprobada", reviewer_note=reviewer_note)


def request_changes(action_id: int, reviewer_note: str) -> None:
    if not reviewer_note.strip():
        raise ValueError("Escribe qué debe modificarse.")
    action = get_action(action_id)
    if not action:
        raise ValueError("Acción inexistente.")
    if action.status == "ejecutada":
        raise ValueError("La acción ya fue ejecutada.")
    set_action_status(action_id, "cambios_solicitados", reviewer_note=reviewer_note.strip())


def reject_action(action_id: int, reviewer_note: str | None = None) -> None:
    action = get_action(action_id)
    if not action:
        raise ValueError("Acción inexistente.")
    if action.status == "ejecutada":
        raise ValueError("La acción ya fue ejecutada.")
    set_action_status(action_id, "rechazada", reviewer_note=reviewer_note)


def execute_action(action_id: int, dry_run: bool = True) -> str:
    action = get_action(action_id)
    if not action:
        raise ValueError("Acción inexistente.")

    if action.status == "rechazada":
        raise PermissionError("Esta acción fue rechazada.")

    # Regla de seguridad:
    # cualquier acción externa debe estar aprobada explícitamente.
    if action.channel in EXTERNAL_CHANNELS and action.status != "aprobada":
        raise PermissionError("Bárbara debe aprobar esta acción antes de ejecutarla.")

    if action.requires_approval and action.status != "aprobada":
        raise PermissionError("Bárbara debe aprobar esta acción antes de ejecutarla.")

    if action.status == "ejecutada":
        return action.execution_result or "La acción ya fue ejecutada."

    if dry_run:
        # Fase 1: no hay conexión directa con Instagram/WhatsApp, así que Bárbara publica o envía ella misma.
        if action.channel == "internal":
            result = f"Hecho · '{action.title}' se registró como realizada."
        else:
            result = (
                f"Lista para {action.channel} · Copia el contenido y publícalo o prográmalo tú "
                f"(en Instagram: Meta Business Suite → Programar). La publicación automática llega en la fase 2."
            )
        set_action_status(action_id, "ejecutada", result=result)
        return result

    # Aquí se agregan los conectores reales en la Fase 2.
    # Ejemplos futuros:
    # if action.channel == "instagram":
    #     result = publish_instagram(action)
    # elif action.channel == "facebook":
    #     result = publish_facebook(action)
    # elif action.channel == "whatsapp":
    #     result = send_whatsapp(action)
    # elif action.channel == "email":
    #     result = send_email(action)
    # else:
    #     result = run_internal_analysis(action)
    #
    # set_action_status(action_id, "ejecutada", result=result)
    # return result

    raise NotImplementedError("La ejecución real todavía no está conectada.")
