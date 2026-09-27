from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    objective: Mapped[str] = mapped_column(Text)
    budget: Mapped[float] = mapped_column(Float, default=0)
    target_leads: Mapped[int] = mapped_column(Integer, default=0)
    target_patients: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    end_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="borrador")
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    actions: Mapped[list["MarketingAction"]] = relationship(
        back_populates="campaign", cascade="all, delete-orphan"
    )


class MarketingAction(Base):
    __tablename__ = "marketing_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    action_type: Mapped[str] = mapped_column(String(50))
    channel: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text, default="")
    scheduled_for: Mapped[str | None] = mapped_column(String(32), nullable=True)
    priority: Mapped[str] = mapped_column(String(20), default="media")
    status: Mapped[str] = mapped_column(String(30), default="propuesta")
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    reviewer_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    execution_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    campaign: Mapped[Campaign] = relationship(back_populates="actions")


class Metric(Base):
    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    action_id: Mapped[int | None] = mapped_column(ForeignKey("marketing_actions.id"), nullable=True)
    metric_name: Mapped[str] = mapped_column(String(80))
    metric_value: Mapped[float] = mapped_column(Float)
    recorded_date: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class LeadEvent(Base):
    """
    Evento de marketing agregado/anónimo.
    NO guardar nombre, RUT, diagnóstico, teléfono ni información clínica.
    """
    __tablename__ = "lead_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"))
    source: Mapped[str] = mapped_column(String(80))
    service_category: Mapped[str] = mapped_column(String(120))
    outcome: Mapped[str] = mapped_column(String(40))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    recorded_date: Mapped[str] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
