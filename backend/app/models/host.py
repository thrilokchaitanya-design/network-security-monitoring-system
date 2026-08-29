from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Host(Base):
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    hostname: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
    )

    mac_address: Mapped[str] = mapped_column(
        String(17),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="online",
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    alerts = relationship(
        "Alert",
        back_populates="host",
    )