from __future__ import annotations

import json
from pydantic import ValidationError

from .schemas import MarketingPlan


# Contrato entre Bárbara.IA (el "cerebro", antes Nexus) y el Executor. Bárbara.IA lo usa para generar
# los planes solo (ver nexus/ia.py, planificar_campana); también sirve para pegar un plan a mano.
NEXUS_OUTPUT_INSTRUCTIONS = """
Cuando Bárbara pida un plan para el ejecutor de marketing, devuelve un JSON válido con esta estructura:

{
  "campaign_name": "Nombre campaña",
  "objective": "Objetivo medible",
  "budget": 0,
  "target_leads": 20,
  "target_patients": 5,
  "start_date": "AAAA-MM-DD",
  "end_date": "AAAA-MM-DD",
  "actions": [
    {
      "action_type": "social_post | story | reel | ad_campaign | follow_up | analysis | email",
      "channel": "instagram | facebook | whatsapp | email | internal",
      "title": "Título corto",
      "content": "Contenido o instrucciones completas",
      "scheduled_for": "AAAA-MM-DDTHH:MM:SS",
      "priority": "baja | media | alta",
      "requires_approval": true
    }
  ]
}

"target_leads" son las consultas esperadas y "target_patients" las nuevas clientas (el nombre del
campo se mantiene por compatibilidad). No ejecutes acciones desde Bárbara.IA: Bárbara.IA propone;
el ejecutor valida, solicita aprobación y ejecuta.
"""


def parse_plan(raw: str | dict) -> MarketingPlan:
    if isinstance(raw, str):
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.replace("```json", "").replace("```", "").strip()
        raw = json.loads(raw)
    try:
        return MarketingPlan.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"El plan no cumple el formato esperado: {exc}") from exc


def example_plan() -> dict:
    return {
        "campaign_name": "Octubre · Crea tu guatero conmigo",
        "objective": "Dar a conocer la experiencia de crear guateros y conseguir 15 consultas y 4 nuevas clientas en Puente Alto.",
        "budget": 0,
        "target_leads": 15,
        "target_patients": 4,
        "start_date": "2026-10-01",
        "end_date": "2026-10-31",
        "actions": [
            {
                "action_type": "reel",
                "channel": "instagram",
                "title": "Reel: así nace un guatero hecho con cariño",
                "content": "Guion preparado por Bárbara.IA mostrando tus manos eligiendo semillas y hierbas. Revisar tono antes de publicar.",
                "scheduled_for": "2026-10-06T19:30:00",
                "priority": "alta",
                "requires_approval": True,
            },
            {
                "action_type": "story",
                "channel": "instagram",
                "title": "Historias: ¿qué te ayuda a desconectarte?",
                "content": "3 historias breves con una pregunta y una invitación a escribir por WhatsApp.",
                "scheduled_for": "2026-10-08T20:00:00",
                "priority": "media",
                "requires_approval": True,
            },
            {
                "action_type": "analysis",
                "channel": "internal",
                "title": "Análisis semanal de resultados",
                "content": "Comparar alcance, consultas y clientas nuevas de la semana.",
                "scheduled_for": "2026-10-11T18:00:00",
                "priority": "media",
                "requires_approval": False,
            },
        ],
    }
