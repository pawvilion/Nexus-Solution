\
from __future__ import annotations

import os
from datetime import datetime, timezone

import streamlit as st
from sqlalchemy import create_engine, delete, func, select, update
from sqlalchemy.orm import sessionmaker

from .models import Base, Campaign, LeadEvent, MarketingAction, Metric


def _database_url() -> str:
    try:
        value = st.secrets.get("DATABASE_URL", "")
        if value:
            return value
    except Exception:
        pass
    return os.getenv("DATABASE_URL", "sqlite:///dalmeet_marketing.db")


DATABASE_URL = _database_url()
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)


# ---------------- CAMPAIGNS ----------------

def create_campaign(
    name: str,
    objective: str,
    budget: float,
    target_leads: int = 0,
    target_patients: int = 0,
    start_date: str | None = None,
    end_date: str | None = None,
    make_active: bool = False,
) -> Campaign:
    with SessionLocal() as db:
        if make_active:
            db.execute(update(Campaign).values(is_active=False))
        row = Campaign(
            name=name,
            objective=objective,
            budget=float(budget or 0),
            target_leads=int(target_leads or 0),
            target_patients=int(target_patients or 0),
            start_date=start_date or None,
            end_date=end_date or None,
            status="activa" if make_active else "borrador",
            is_active=make_active,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row


def list_campaigns() -> list[Campaign]:
    with SessionLocal() as db:
        return list(db.scalars(select(Campaign).order_by(Campaign.id.desc())).all())


def get_campaign(campaign_id: int) -> Campaign | None:
    with SessionLocal() as db:
        return db.get(Campaign, campaign_id)


def get_active_campaign() -> Campaign | None:
    with SessionLocal() as db:
        return db.scalar(select(Campaign).where(Campaign.is_active.is_(True)))


def set_active_campaign(campaign_id: int) -> None:
    with SessionLocal() as db:
        db.execute(update(Campaign).values(is_active=False))
        row = db.get(Campaign, campaign_id)
        if not row:
            raise ValueError("Campaña no encontrada.")
        row.is_active = True
        row.status = "activa"
        db.commit()


def update_campaign_status(campaign_id: int, status: str) -> None:
    with SessionLocal() as db:
        row = db.get(Campaign, campaign_id)
        if not row:
            raise ValueError("Campaña no encontrada.")
        row.status = status
        if status != "activa":
            row.is_active = False
        db.commit()


# ---------------- ACTIONS ----------------

def add_action(
    campaign_id: int,
    action_type: str,
    channel: str,
    title: str,
    content: str = "",
    scheduled_for: str | None = None,
    priority: str = "media",
    requires_approval: bool = True,
) -> MarketingAction:
    with SessionLocal() as db:
        row = MarketingAction(
            campaign_id=campaign_id,
            action_type=action_type,
            channel=channel,
            title=title,
            content=content or "",
            scheduled_for=scheduled_for or None,
            priority=priority,
            requires_approval=requires_approval,
            status="propuesta" if requires_approval else "aprobada",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row


def list_actions(campaign_id: int | None = None) -> list[MarketingAction]:
    with SessionLocal() as db:
        stmt = select(MarketingAction).order_by(MarketingAction.id.desc())
        if campaign_id is not None:
            stmt = stmt.where(MarketingAction.campaign_id == campaign_id)
        return list(db.scalars(stmt).all())


def get_action(action_id: int) -> MarketingAction | None:
    with SessionLocal() as db:
        return db.get(MarketingAction, action_id)


def update_action(
    action_id: int,
    *,
    title: str | None = None,
    content: str | None = None,
    scheduled_for: str | None = None,
    priority: str | None = None,
    reviewer_note: str | None = None,
    status: str | None = None,
) -> None:
    with SessionLocal() as db:
        row = db.get(MarketingAction, action_id)
        if not row:
            raise ValueError("Acción no encontrada.")
        if title is not None:
            row.title = title
        if content is not None:
            row.content = content
        if scheduled_for is not None:
            row.scheduled_for = scheduled_for or None
        if priority is not None:
            row.priority = priority
        if reviewer_note is not None:
            row.reviewer_note = reviewer_note
        if status is not None:
            row.status = status
        db.commit()


def set_action_status(
    action_id: int,
    status: str,
    result: str | None = None,
    reviewer_note: str | None = None,
) -> None:
    with SessionLocal() as db:
        row = db.get(MarketingAction, action_id)
        if not row:
            raise ValueError("Acción no encontrada.")
        row.status = status
        if reviewer_note is not None:
            row.reviewer_note = reviewer_note
        if status == "ejecutada":
            row.executed_at = datetime.now(timezone.utc)
        if result is not None:
            row.execution_result = result
        db.commit()


# ---------------- METRICS ----------------

def add_metric(
    campaign_id: int,
    action_id: int | None,
    metric_name: str,
    metric_value: float,
    recorded_date: str,
) -> None:
    with SessionLocal() as db:
        db.add(
            Metric(
                campaign_id=campaign_id,
                action_id=action_id,
                metric_name=metric_name,
                metric_value=float(metric_value),
                recorded_date=recorded_date,
            )
        )
        db.commit()


def list_metrics(campaign_id: int | None = None) -> list[Metric]:
    with SessionLocal() as db:
        stmt = select(Metric).order_by(Metric.recorded_date.asc(), Metric.id.asc())
        if campaign_id is not None:
            stmt = stmt.where(Metric.campaign_id == campaign_id)
        return list(db.scalars(stmt).all())


def metric_total(campaign_id: int, metric_name: str) -> float:
    with SessionLocal() as db:
        value = db.scalar(
            select(func.coalesce(func.sum(Metric.metric_value), 0.0)).where(
                Metric.campaign_id == campaign_id,
                Metric.metric_name == metric_name,
            )
        )
        return float(value or 0)


# ---------------- LEAD EVENTS ----------------

def add_lead_event(
    campaign_id: int,
    source: str,
    service_category: str,
    outcome: str,
    quantity: int,
    recorded_date: str,
) -> None:
    with SessionLocal() as db:
        db.add(
            LeadEvent(
                campaign_id=campaign_id,
                source=source,
                service_category=service_category,
                outcome=outcome,
                quantity=int(quantity),
                recorded_date=recorded_date,
            )
        )
        db.commit()


def list_lead_events(campaign_id: int | None = None) -> list[LeadEvent]:
    with SessionLocal() as db:
        stmt = select(LeadEvent).order_by(LeadEvent.recorded_date.asc(), LeadEvent.id.asc())
        if campaign_id is not None:
            stmt = stmt.where(LeadEvent.campaign_id == campaign_id)
        return list(db.scalars(stmt).all())


def lead_total(campaign_id: int, outcome: str | None = None) -> int:
    with SessionLocal() as db:
        stmt = select(func.coalesce(func.sum(LeadEvent.quantity), 0)).where(
            LeadEvent.campaign_id == campaign_id
        )
        if outcome:
            stmt = stmt.where(LeadEvent.outcome == outcome)
        return int(db.scalar(stmt) or 0)
