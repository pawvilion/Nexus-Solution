\
from __future__ import annotations

import json
from pydantic import ValidationError

from .schemas import MarketingPlan


NEXUS_OUTPUT_INSTRUCTIONS = """
Cuando el usuario pida enviar un plan al ejecutor de marketing, devuelve además
un JSON válido con esta estructura:

{
  "campaign_name": "Nombre campaña",
  "objective": "Objetivo medible",
  "budget": 80000,
  "target_leads": 20,
  "target_patients": 8,
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

No ejecutes acciones desde Nexus. Nexus propone; el ejecutor valida, solicita
aprobación y ejecuta.
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
        "campaign_name": "Octubre · Terapia ocupacional",
        "objective": "Aumentar consultas calificadas y convertirlas en nuevas reservas.",
        "budget": 100000,
        "target_leads": 25,
        "target_patients": 10,
        "start_date": "2026-10-01",
        "end_date": "2026-10-31",
        "actions": [
            {
                "action_type": "reel",
                "channel": "instagram",
                "title": "Reel educativo: señales para consultar",
                "content": "Guion educativo preparado por Nexus. Revisar tono y afirmaciones antes de publicar.",
                "scheduled_for": "2026-10-05T19:00:00",
                "priority": "alta",
                "requires_approval": True,
            },
            {
                "action_type": "story",
                "channel": "instagram",
                "title": "Historia con preguntas frecuentes",
                "content": "3 historias breves con FAQ y CTA hacia el canal de contacto.",
                "scheduled_for": "2026-10-08T20:00:00",
                "priority": "media",
                "requires_approval": True,
            },
            {
                "action_type": "analysis",
                "channel": "internal",
                "title": "Análisis semanal de resultados",
                "content": "Comparar alcance, consultas, reservas y gasto de la semana.",
                "scheduled_for": "2026-10-11T18:00:00",
                "priority": "media",
                "requires_approval": False,
            },
        ],
    }
