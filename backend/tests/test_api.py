"""API tests for the backend.

Each test uses an isolated in-memory SQLite database so the suite never touches
the real gym.db file. Covers the happy path and validation for every endpoint,
satisfying the Phase 2 "perform adequate software tests" requirement.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Equipment


@pytest.fixture()
def client():
    """Provide a TestClient backed by a fresh in-memory database per test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    # Pre-load a couple of equipment rows to report against.
    db = TestingSession()
    db.add_all([
        Equipment(name="Treadmill #1", category="Cardio", location="Cardio Zone"),
        Equipment(name="Leg Press", category="Strength", location="Strength Floor"),
    ])
    db.commit()
    db.close()

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_list_equipment(client):
    res = client.get("/equipment")
    assert res.status_code == 200
    names = [e["name"] for e in res.json()]
    assert "Treadmill #1" in names and len(names) == 2


def test_create_ticket_succeeds(client):
    res = client.post("/tickets", json={"equipment_id": 1, "description": "Belt slips badly."})
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "Open"
    assert body["equipment"]["name"] == "Treadmill #1"


def test_create_ticket_rejects_empty_description(client):
    res = client.post("/tickets", json={"equipment_id": 1, "description": ""})
    assert res.status_code == 422  # FR-03 validation


def test_create_ticket_rejects_unknown_equipment(client):
    res = client.post("/tickets", json={"equipment_id": 999, "description": "Does not exist."})
    assert res.status_code == 404


def test_update_ticket_status(client):
    created = client.post(
        "/tickets", json={"equipment_id": 2, "description": "Pin is bent."}
    ).json()
    res = client.patch(f"/tickets/{created['id']}", json={"status": "In Progress"})
    assert res.status_code == 200
    assert res.json()["status"] == "In Progress"


def test_list_tickets_returns_created(client):
    client.post("/tickets", json={"equipment_id": 1, "description": "Screen flickers."})
    res = client.get("/tickets")
    assert res.status_code == 200
    assert len(res.json()) == 1
