from datetime import datetime

from sqlalchemy.orm import Session

from app.api.websocket import manager
from app.models.alert import Alert


async def create_alert(
    db: Session,
    severity: str,
    attack_type: str,
    source_ip: str,
    destination_ip: str,
    confidence_score: float | None = None,
    status: str = "active",
    description: str | None = None,
    host_id: int | None = None,
):
    alert = Alert(
        severity=severity,
        attack_type=attack_type,
        source_ip=source_ip,
        destination_ip=destination_ip,
        confidence_score=confidence_score,
        status=status,
        description=description,
        host_id=host_id,
        timestamp=datetime.utcnow(),
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    message = {
        "type": "alert",
        "data": {
            "id": alert.id,
            "severity": alert.severity,
            "attack_type": alert.attack_type,
            "source_ip": alert.source_ip,
            "destination_ip": alert.destination_ip,
            "confidence_score": alert.confidence_score,
            "timestamp": alert.timestamp.isoformat(),
            "status": alert.status,
            "description": alert.description,
            "host_id": alert.host_id,
        },
    }

    await manager.broadcast(message)

    return alert