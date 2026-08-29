from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    attack_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    source_ip: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
    )

    destination_ip: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
    )

    host_id: Mapped[int | None] = mapped_column(
        ForeignKey("hosts.id"),
        nullable=True,
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    host = relationship(
        "Host",
        back_populates="alerts",
    )

    actions = relationship(
        "AlertAction",
        back_populates="alert",
        cascade="all, delete-orphan",
    )