from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_topology():
    response = client.get("/topology")

    assert response.status_code == 200

    data = response.json()

    assert "nodes" in data
    assert "links" in data

    assert isinstance(data["nodes"], list)
    assert isinstance(data["links"], list)

    # The topology should contain the logical switch.
    switch = next(
        (
            node
            for node in data["nodes"]
            if node.get("type") == "switch"
        ),
        None,
    )

    assert switch is not None
    assert switch["id"] == "switch-1"


def test_topology_node_structure():
    response = client.get("/topology")

    assert response.status_code == 200

    data = response.json()

    for node in data["nodes"]:
        assert "id" in node
        assert "type" in node


def test_topology_link_structure():
    response = client.get("/topology")

    assert response.status_code == 200

    data = response.json()

    for link in data["links"]:
        assert "source" in link
        assert "target" in link


def test_topology_uses_configured_controller(monkeypatch):
    from app.api import topology

    monkeypatch.setenv("SDN_CONTROLLER_URL", "http://controller")
    responses = {
        "/v1.0/topology/switches": [{"dpid": "0000000000000001", "name": "s1"}],
        "/v1.0/topology/links": [],
        "/v1.0/topology/hosts": [{"mac": "00:00:00:00:00:01", "ipv4": ["10.0.0.1"], "port": {"dpid": "0000000000000001", "port_no": "2"}}],
    }
    monkeypatch.setattr(topology, "_controller_get", lambda _url, path: responses[path])

    response = client.get("/topology")
    assert response.status_code == 200
    data = response.json()
    assert data["source"] == "sdn_controller"
    assert any(node["type"] == "switch" and node["name"] == "s1" for node in data["nodes"])
    assert any(node["type"] == "host" and node["ip_address"] == "10.0.0.1" for node in data["nodes"])
    assert data["links"] == [{"source": "host-00:00:00:00:00:01", "target": "switch-0000000000000001", "port": "2"}]
