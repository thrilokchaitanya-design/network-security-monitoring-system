import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from fastapi import APIRouter, Depends, HTTPException
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
    """Return live Ryu topology when configured, otherwise registered hosts."""
    controller_url = os.getenv("SDN_CONTROLLER_URL", "").rstrip("/")
    if controller_url:
        try:
            switches = _controller_get(controller_url, "/v1.0/topology/switches")
            links_data = _controller_get(controller_url, "/v1.0/topology/links")
            hosts_data = _controller_get(controller_url, "/v1.0/topology/hosts")
            nodes = [
                {"id": f"switch-{item['dpid']}", "type": "switch", "name": item.get("name") or item["dpid"], "dpid": item["dpid"], "status": "online"}
                for item in switches
            ]
            for item in hosts_data:
                address = (item.get("ipv4") or [None])[0]
                nodes.append({"id": f"host-{item['mac']}", "type": "host", "hostname": item.get("name") or item["mac"], "ip_address": address, "mac_address": item["mac"], "status": "online"})
            links = [
                {"source": f"switch-{item['src']['dpid']}", "target": f"switch-{item['dst']['dpid']}", "source_port": item["src"].get("port_no"), "target_port": item["dst"].get("port_no")}
                for item in links_data
            ]
            for item in hosts_data:
                attachments = item.get("port") or []
                if isinstance(attachments, dict):
                    attachments = [attachments]
                for attachment in attachments:
                    links.append({"source": f"host-{item['mac']}", "target": f"switch-{attachment['dpid']}", "port": attachment.get("port_no")})
            return {"source": "sdn_controller", "nodes": nodes, "links": links}
        except (KeyError, TypeError, ValueError, HTTPException) as exc:
            if isinstance(exc, HTTPException):
                raise
            raise HTTPException(status_code=502, detail=f"Invalid topology response from SDN controller: {exc}") from exc

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
        "source": "registered_hosts",
        "nodes": nodes,
        "links": links,
    }


def _controller_get(base_url: str, path: str):
    try:
        with urlopen(f"{base_url}{path}", timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail=f"Could not read SDN controller topology ({path}): {exc}") from exc
