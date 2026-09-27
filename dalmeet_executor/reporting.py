from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime

from .db import (
    get_campaign,
    lead_total,
    list_actions,
    list_lead_events,
    list_metrics,
    metric_total,
)


def build_campaign_summary(campaign_id: int) -> dict:
    campaign = get_campaign(campaign_id)
    if not campaign:
        raise ValueError("Campaña no encontrada.")

    actions = list_actions(campaign_id)
    metrics = list_metrics(campaign_id)
    leads = list_lead_events(campaign_id)

    consultations = lead_total(campaign_id, "consulta")
    appointments = lead_total(campaign_id, "agendado")
    patients = lead_total(campaign_id, "paciente")
    spend = metric_total(campaign_id, "gasto")
    reach = metric_total(campaign_id, "alcance")
    impressions = metric_total(campaign_id, "impresiones")
    clicks = metric_total(campaign_id, "clics")

    total_lead_events = sum(x.quantity for x in leads)
    conversion = (patients / consultations * 100) if consultations else 0
    cac = (spend / patients) if patients else None
    cost_per_consultation = (spend / consultations) if consultations else None

    by_source = defaultdict(lambda: {"consultas": 0, "agendados": 0, "pacientes": 0})
    for x in leads:
        if x.outcome == "consulta":
            by_source[x.source]["consultas"] += x.quantity
        elif x.outcome == "agendado":
            by_source[x.source]["agendados"] += x.quantity
        elif x.outcome == "paciente":
            by_source[x.source]["pacientes"] += x.quantity

    return {
        "campaign": {
            "id": campaign.id,
            "name": campaign.name,
            "objective": campaign.objective,
            "budget": campaign.budget,
            "target_leads": campaign.target_leads,
            "target_patients": campaign.target_patients,
            "start_date": campaign.start_date,
            "end_date": campaign.end_date,
            "status": campaign.status,
        },
        "execution": {
            "total_actions": len(actions),
            "executed_actions": sum(a.status == "ejecutada" for a in actions),
            "pending_approval": sum(a.status == "propuesta" for a in actions),
            "changes_requested": sum(a.status == "cambios_solicitados" for a in actions),
            "rejected": sum(a.status == "rechazada" for a in actions),
        },
        "results": {
            "reach": reach,
            "impressions": impressions,
            "clicks": clicks,
            "consultations": consultations,
            "appointments": appointments,
            "patients": patients,
            "spend": spend,
            "conversion_consultation_to_patient_pct": round(conversion, 2),
            "cost_per_consultation": round(cost_per_consultation, 2) if cost_per_consultation is not None else None,
            "cac": round(cac, 2) if cac is not None else None,
        },
        "by_source": dict(by_source),
    }


def build_nexus_report(campaign_id: int) -> str:
    data = build_campaign_summary(campaign_id)
    c = data["campaign"]
    e = data["execution"]
    r = data["results"]

    def money(value):
        if value is None:
            return "N/D"
        return f"${value:,.0f}".replace(",", ".")

    lines = [
        "REPORTE DE RETROALIMENTACIÓN PARA BÁRBARA.IA",
        "",
        f"Campaña: {c['name']}",
        f"Objetivo: {c['objective']}",
        f"Periodo: {c['start_date'] or 'N/D'} a {c['end_date'] or 'N/D'}",
        f"Presupuesto definido: {money(c['budget'])}",
        "",
        "EJECUCIÓN",
        f"- Acciones totales: {e['total_actions']}",
        f"- Acciones ejecutadas: {e['executed_actions']}",
        f"- Pendientes de aprobación: {e['pending_approval']}",
        f"- Con cambios solicitados: {e['changes_requested']}",
        "",
        "RESULTADOS",
        f"- Alcance: {r['reach']:,.0f}",
        f"- Impresiones: {r['impressions']:,.0f}",
        f"- Clics: {r['clicks']:,.0f}",
        f"- Consultas: {r['consultations']}",
        f"- Agendamientos: {r['appointments']}",
        f"- Nuevas clientas: {r['patients']}",
        f"- Gasto: {money(r['spend'])}",
        f"- Conversión consulta → clienta: {r['conversion_consultation_to_patient_pct']:.1f}%",
        f"- Costo por consulta: {money(r['cost_per_consultation'])}",
        f"- CAC: {money(r['cac'])}",
        "",
        "RESULTADOS POR CANAL / ORIGEN",
    ]

    if data["by_source"]:
        for source, values in sorted(data["by_source"].items()):
            lines.append(
                f"- {source}: {values['consultas']} consultas, "
                f"{values['agendados']} agendamientos, "
                f"{values['pacientes']} nuevas clientas."
            )
    else:
        lines.append("- Aún no hay datos registrados por origen.")

    lines += [
        "",
        "INSTRUCCIÓN PARA BÁRBARA.IA",
        "Analiza estos resultados junto con el objetivo original. Identifica qué mantener, "
        "qué modificar y qué eliminar. Propón el siguiente ciclo de marketing y devuelve "
        "el nuevo plan en el formato JSON del Marketing Executor. No ejecutes acciones.",
    ]
    return "\n".join(lines)


def build_nexus_json(campaign_id: int) -> str:
    return json.dumps(build_campaign_summary(campaign_id), ensure_ascii=False, indent=2)
