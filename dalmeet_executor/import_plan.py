from __future__ import annotations

from .brain_adapter import parse_plan
from .db import add_action, create_campaign


def save_nexus_plan(raw_plan: str | dict, make_active: bool = True) -> int:
    plan = parse_plan(raw_plan)

    campaign = create_campaign(
        name=plan.campaign_name,
        objective=plan.objective,
        budget=plan.budget,
        target_leads=plan.target_leads,
        target_patients=plan.target_patients,
        start_date=plan.start_date,
        end_date=plan.end_date,
        make_active=make_active,
    )

    for action in plan.actions:
        add_action(
            campaign_id=campaign.id,
            action_type=action.action_type,
            channel=action.channel,
            title=action.title,
            content=action.content,
            scheduled_for=action.scheduled_for,
            priority=action.priority,
            requires_approval=action.requires_approval,
        )

    return campaign.id
