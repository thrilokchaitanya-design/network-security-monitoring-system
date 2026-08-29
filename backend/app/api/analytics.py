from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert


router = APIRouter(
    prefix="/analytics",
    tags=["Security Analytics"],
)


# ============================================================
# SECURITY SUMMARY
# ============================================================

@router.get("/summary")
def get_security_summary(
    db: Session = Depends(get_db),
):
    total_alerts = (
        db.query(func.count(Alert.id))
        .scalar()
        or 0
    )

    active_alerts = (
        db.query(func.count(Alert.id))
        .filter(
            Alert.status.in_(
                ["active", "investigating"]
            )
        )
        .scalar()
        or 0
    )

    resolved_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.status == "resolved")
        .scalar()
        or 0
    )

    critical_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.severity == "CRITICAL")
        .scalar()
        or 0
    )

    high_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.severity == "HIGH")
        .scalar()
        or 0
    )

    medium_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.severity == "MEDIUM")
        .scalar()
        or 0
    )

    low_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.severity == "LOW")
        .scalar()
        or 0
    )

    average_confidence = (
        db.query(func.avg(Alert.confidence_score))
        .filter(Alert.confidence_score.isnot(None))
        .scalar()
    )

    return {
        "total_alerts": total_alerts,
        "active_alerts": active_alerts,
        "resolved_alerts": resolved_alerts,
        "severity": {
            "critical": critical_alerts,
            "high": high_alerts,
            "medium": medium_alerts,
            "low": low_alerts,
        },
        "average_confidence": (
            round(float(average_confidence), 4)
            if average_confidence is not None
            else None
        ),
    }


# ============================================================
# ATTACK TYPE DISTRIBUTION
# ============================================================

@router.get("/attacks")
def get_attack_distribution(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Alert.attack_type,
            func.count(Alert.id).label("count"),
        )
        .group_by(Alert.attack_type)
        .order_by(func.count(Alert.id).desc())
        .all()
    )

    return [
        {
            "attack_type": attack_type,
            "count": count,
        }
        for attack_type, count in results
    ]


# ============================================================
# SEVERITY DISTRIBUTION
# ============================================================

@router.get("/severity")
def get_severity_distribution(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Alert.severity,
            func.count(Alert.id).label("count"),
        )
        .group_by(Alert.severity)
        .order_by(func.count(Alert.id).desc())
        .all()
    )

    return [
        {
            "severity": severity,
            "count": count,
        }
        for severity, count in results
    ]


# ============================================================
# TOP ATTACK SOURCES
# ============================================================

@router.get("/sources")
def get_attack_sources(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            Alert.source_ip,
            func.count(Alert.id).label("count"),
        )
        .group_by(Alert.source_ip)
        .order_by(func.count(Alert.id).desc())
        .limit(10)
        .all()
    )

    return [
        {
            "source_ip": source_ip,
            "count": count,
        }
        for source_ip, count in results
    ]