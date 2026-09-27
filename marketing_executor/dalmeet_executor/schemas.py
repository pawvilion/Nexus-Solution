\
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


ActionType = Literal[
    "social_post",
    "story",
    "reel",
    "ad_campaign",
    "follow_up",
    "analysis",
    "email",
]

ChannelType = Literal[
    "instagram",
    "facebook",
    "whatsapp",
    "email",
    "internal",
]

PriorityType = Literal["baja", "media", "alta"]


class ActionProposal(BaseModel):
    action_type: ActionType
    channel: ChannelType
    title: str = Field(min_length=3, max_length=200)
    content: str = ""
    scheduled_for: str | None = None
    priority: PriorityType = "media"
    requires_approval: bool = True


class MarketingPlan(BaseModel):
    campaign_name: str = Field(min_length=3, max_length=200)
    objective: str = Field(min_length=3)
    budget: float = Field(default=0, ge=0)
    target_leads: int = Field(default=0, ge=0)
    target_patients: int = Field(default=0, ge=0)
    start_date: str | None = None
    end_date: str | None = None
    actions: list[ActionProposal] = Field(default_factory=list)
