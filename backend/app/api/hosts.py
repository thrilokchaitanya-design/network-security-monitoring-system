from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import get_current_analyst, get_current_admin
from app.database import get_db
from app.models.host import Host as HostModel
from app.models.alert import Alert as AlertModel
from app.models.user import User


router = APIRouter(
    prefix="/hosts",
    tags=["Hosts"],
)


# ============================================================
# SCHEMAS
# ============================================================

class HostCreate(BaseModel):
    hostname: str
    ip_address: str
    mac_address: str
    status: str = "online"
    risk_score: float = 0.0


class HostUpdate(BaseModel):
    hostname: str | None = None
    ip_address: str | None = None
    mac_address: str | None = None
    status: str | None = None
    risk_score: float | None = None


class HostResponse(BaseModel):
    id: int
    hostname: str
    ip_address: str
    mac_address: str
    status: str
    risk_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    severity: str
    attack_type: str
    source_ip: str
    destination_ip: str
    confidence_score: float | None
    timestamp: datetime
    status: str
    description: str | None
    host_id: int | None

    class Config:
        from_attributes = True


# ============================================================
# GET ALL HOSTS
# Access: Analyst + Admin
# ============================================================

@router.get(
    "",
    response_model=List[HostResponse],
)
def get_hosts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst),
):
    return (
        db.query(HostModel)
        .order_by(HostModel.id.asc())
        .all()
    )


# ============================================================
# CREATE HOST
# Access: Admin only
# ============================================================

@router.post(
    "",
    response_model=HostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_host(
    host_data: HostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    # Check duplicate hostname
    existing_hostname = (
        db.query(HostModel)
        .filter(HostModel.hostname == host_data.hostname)
        .first()
    )

    if existing_hostname:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Hostname already exists",
        )

    # Check duplicate IP
    existing_ip = (
        db.query(HostModel)
        .filter(HostModel.ip_address == host_data.ip_address)
        .first()
    )

    if existing_ip:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="IP address already exists",
        )

    # Check duplicate MAC
    existing_mac = (
        db.query(HostModel)
        .filter(HostModel.mac_address == host_data.mac_address)
        .first()
    )

    if existing_mac:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="MAC address already exists",
        )

    host = HostModel(
        hostname=host_data.hostname,
        ip_address=host_data.ip_address,
        mac_address=host_data.mac_address,
        status=host_data.status,
        risk_score=host_data.risk_score,
    )

    db.add(host)
    db.commit()
    db.refresh(host)

    return host


# ============================================================
# GET HOST BY ID
# Access: Analyst + Admin
# ============================================================

@router.get(
    "/{host_id}",
    response_model=HostResponse,
)
def get_host(
    host_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst),
):
    host = (
        db.query(HostModel)
        .filter(HostModel.id == host_id)
        .first()
    )

    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Host not found",
        )

    return host


# ============================================================
# UPDATE HOST
# Access: Admin only
# ============================================================

@router.patch(
    "/{host_id}",
    response_model=HostResponse,
)
def update_host(
    host_id: int,
    host_data: HostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    host = (
        db.query(HostModel)
        .filter(HostModel.id == host_id)
        .first()
    )

    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Host not found",
        )

    update_data = host_data.model_dump(
        exclude_unset=True
    )

    # Check hostname conflict
    if "hostname" in update_data:
        existing = (
            db.query(HostModel)
            .filter(
                HostModel.hostname == update_data["hostname"],
                HostModel.id != host_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Hostname already exists",
            )

    # Check IP conflict
    if "ip_address" in update_data:
        existing = (
            db.query(HostModel)
            .filter(
                HostModel.ip_address == update_data["ip_address"],
                HostModel.id != host_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="IP address already exists",
            )

    # Check MAC conflict
    if "mac_address" in update_data:
        existing = (
            db.query(HostModel)
            .filter(
                HostModel.mac_address == update_data["mac_address"],
                HostModel.id != host_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="MAC address already exists",
            )

    for field, value in update_data.items():
        setattr(host, field, value)

    host.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(host)

    return host


# ============================================================
# GET ALERTS FOR HOST
# Access: Analyst + Admin
# ============================================================

@router.get(
    "/{host_id}/alerts",
    response_model=List[AlertResponse],
)
def get_host_alerts(
    host_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst),
):
    host = (
        db.query(HostModel)
        .filter(HostModel.id == host_id)
        .first()
    )

    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Host not found",
        )

    return (
        db.query(AlertModel)
        .filter(AlertModel.host_id == host_id)
        .order_by(AlertModel.timestamp.desc())
        .all()
    )


# ============================================================
# SECURITY SUMMARY
# Access: Analyst + Admin
# ============================================================

@router.get(
    "/{host_id}/security-summary",
)
def get_security_summary(
    host_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst),
):
    host = (
        db.query(HostModel)
        .filter(HostModel.id == host_id)
        .first()
    )

    if not host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Host not found",
        )

    alerts = (
        db.query(AlertModel)
        .filter(AlertModel.host_id == host_id)
        .all()
    )

    total_alerts = len(alerts)

    active_alerts = sum(
        1
        for alert in alerts
        if alert.status.lower() == "active"
    )

    resolved_alerts = sum(
        1
        for alert in alerts
        if alert.status.lower() == "resolved"
    )

    critical_alerts = sum(
        1
        for alert in alerts
        if alert.severity.upper() == "CRITICAL"
    )

    high_alerts = sum(
        1
        for alert in alerts
        if alert.severity.upper() == "HIGH"
    )

    medium_alerts = sum(
        1
        for alert in alerts
        if alert.severity.upper() == "MEDIUM"
    )

    low_alerts = sum(
        1
        for alert in alerts
        if alert.severity.upper() == "LOW"
    )

    confidence_values = [
        alert.confidence_score
        for alert in alerts
        if alert.confidence_score is not None
    ]

    average_confidence = (
        round(
            sum(confidence_values)
            / len(confidence_values),
            4,
        )
        if confidence_values
        else 0.0
    )

    return {
        "host": {
            "id": host.id,
            "hostname": host.hostname,
            "ip_address": host.ip_address,
            "mac_address": host.mac_address,
            "status": host.status,
            "risk_score": host.risk_score,
        },
        "security": {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "severity": {
                "critical": critical_alerts,
                "high": high_alerts,
                "medium": medium_alerts,
                "low": low_alerts,
            },
            "average_confidence": average_confidence,
        },
    }