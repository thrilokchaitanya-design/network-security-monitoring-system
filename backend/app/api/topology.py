from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.host import Host


router = APIRouter(
    prefix="/topology",
    tags=["Topology"],
)


# ============================================================
# TOPOLOGY RESPONSE
# ============================================================

@router.get("")
def get_topology(
    db: Session = Depends(get_db),
):
    """
    Return the current monitored network topology.

    The current implementation derives topology information
    from the hosts stored in the database.

    A logical switch node is included as the central network
    element. Real SDN topology information can replace this
    later without changing the frontend API structure.
    """

    hosts = (
        db.query(Host)
        .order_by(Host.id)
        .all()
    )

    nodes = []

    # --------------------------------------------------------
    # Logical switch
    # --------------------------------------------------------

    nodes.append(
        {
            "id": "switch-1",
            "type": "switch",
            "name": "SW-01",
            "status": "online",
        }
    )

    links = []

    # --------------------------------------------------------
    # Host nodes
    # --------------------------------------------------------

    for host in hosts:

        nodes.append(
            {
                "id": f"host-{host.id}",
                "type": "host",
                "hostname": host.hostname,
                "ip_address": host.ip_address,
                "mac_address": host.mac_address,
                "status": host.status,
                "risk_score": host.risk_score,
            }
        )

        links.append(
            {
                "source": f"host-{host.id}",
                "target": "switch-1",
            }
        )

    return {
        "nodes": nodes,
        "links": links,
    }