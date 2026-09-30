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