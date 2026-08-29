from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert as AlertModel
from app.models.host import Host as HostModel
from app.services.alert_service import create_alert as create_alert_service


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


# ============================================================
# SCHEMAS
# ============================================================

class AlertCreate(BaseModel):
    severity: str
    attack_type: str
    source_ip: str
    destination_ip: str
    confidence_score: float | None = None
    status: str
    description: str | None = None
    host_id: int | None = None


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


class AlertListResponse(BaseModel):
    items: List[AlertResponse]
    total: int
    skip: int
    limit: int


# ============================================================
# CREATE ALERT
# ============================================================

@router.post(
    "",
    response_model=AlertResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Validate host if host_id is provided
    # --------------------------------------------------------

    if alert_data.host_id is not None:
        host = (
            db.query(HostModel)
            .filter(HostModel.id == alert_data.host_id)
            .first()
        )

        if not host:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Host not found",
            )

    # --------------------------------------------------------
    # Create alert through service layer
    # --------------------------------------------------------

    alert = await create_alert_service(
        db=db,
        severity=alert_data.severity,
        attack_type=alert_data.attack_type,
        source_ip=alert_data.source_ip,
        destination_ip=alert_data.destination_ip,
        confidence_score=alert_data.confidence_score,
        status=alert_data.status,
        description=alert_data.description,
        host_id=alert_data.host_id,
    )

    return alert


# ============================================================
# GET ALERTS
# ============================================================

@router.get(
    "",
    response_model=AlertListResponse,
)
def get_alerts(
    severity: str | None = Query(
        default=None,
        description="Filter by severity",
    ),
    alert_status: str | None = Query(
        default=None,
        alias="status",
        description="Filter by alert status",
    ),
    host_id: int | None = Query(
        default=None,
        description="Filter by host ID",
    ),
    attack_type: str | None = Query(
        default=None,
        description="Filter by attack type",
    ),
    source_ip: str | None = Query(
        default=None,
        description="Filter by source IP",
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of alerts to skip",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of alerts to return",
    ),
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Base query
    # --------------------------------------------------------

    query = db.query(AlertModel)

    # --------------------------------------------------------
    # Filters
    # --------------------------------------------------------

    if severity:
        query = query.filter(
            AlertModel.severity == severity
        )

    if alert_status:
        query = query.filter(
            AlertModel.status == alert_status
        )

    if host_id is not None:
        query = query.filter(
            AlertModel.host_id == host_id
        )

    if attack_type:
        query = query.filter(
            AlertModel.attack_type == attack_type
        )

    if source_ip:
        query = query.filter(
            AlertModel.source_ip == source_ip
        )

    # --------------------------------------------------------
    # Total matching alerts
    # --------------------------------------------------------

    total = query.count()

    # --------------------------------------------------------
    # Pagination + ordering
    # --------------------------------------------------------

    alerts = (
        query
        .order_by(AlertModel.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "items": alerts,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


# ============================================================
# GET RECENT ALERTS
# ============================================================

@router.get(
    "/recent",
    response_model=List[AlertResponse],
)
def get_recent_alerts(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Number of recent alerts to return",
    ),
    db: Session = Depends(get_db),
):
    alerts = (
        db.query(AlertModel)
        .order_by(AlertModel.timestamp.desc())
        .limit(limit)
        .all()
    )

    return alerts


# ============================================================
# GET ALERT BY ID
# ============================================================

@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = (
        db.query(AlertModel)
        .filter(AlertModel.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    return alert