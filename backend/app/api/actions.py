from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.auth import get_current_analyst
from app.database import get_db
from app.models.alert import Alert
from app.models.alert_action import AlertAction
from app.models.user import User


router = APIRouter(
    prefix="/alerts",
    tags=["Alert Actions"],
)


# ============================================================
# SCHEMAS
# ============================================================

class AlertActionCreate(BaseModel):
    action: str
    details: str | None = None


class AlertActionResponse(BaseModel):
    id: int
    alert_id: int
    action: str
    performed_by: str
    details: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# CREATE ALERT ACTION
# ============================================================

@router.post(
    "/{alert_id}/actions",
    response_model=AlertActionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_alert_action(
    alert_id: int,
    action_data: AlertActionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_analyst),
):
    # --------------------------------------------------------
    # Find alert
    # --------------------------------------------------------

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    # --------------------------------------------------------
    # Validate action
    # --------------------------------------------------------

    allowed_actions = {
        "ACKNOWLEDGED",
        "INVESTIGATING",
        "MITIGATED",
        "RESOLVED",
    }

    action_name = action_data.action.upper()

    if action_name not in allowed_actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Invalid action. Allowed actions: "
                "ACKNOWLEDGED, INVESTIGATING, MITIGATED, RESOLVED"
            ),
        )

    # --------------------------------------------------------
    # Map action -> alert status
    # --------------------------------------------------------

    status_mapping = {
        "ACKNOWLEDGED": "acknowledged",
        "INVESTIGATING": "investigating",
        "MITIGATED": "mitigated",
        "RESOLVED": "resolved",
    }

    # --------------------------------------------------------
    # Create action
    # --------------------------------------------------------
    # performed_by comes from the authenticated JWT user.
    # The client cannot choose another username.

    action = AlertAction(
        alert_id=alert_id,
        action=action_name,
        performed_by=current_user.username,
        details=action_data.details,
        created_at=datetime.utcnow(),
    )

    db.add(action)

    # --------------------------------------------------------
    # Update alert status
    # --------------------------------------------------------

    alert.status = status_mapping[action_name]

    db.commit()
    db.refresh(action)

    return action


# ============================================================
# GET ALERT ACTIONS
# ============================================================

@router.get(
    "/{alert_id}/actions",
    response_model=List[AlertActionResponse],
)
def get_alert_actions(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )

    actions = (
        db.query(AlertAction)
        .filter(AlertAction.alert_id == alert_id)
        .order_by(AlertAction.created_at.asc())
        .all()
    )

    return actions