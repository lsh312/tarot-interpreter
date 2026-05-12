import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_daily_reading(client):
    response = client.post("/reading/daily")
    assert response.status_code == 200
    data = response.json()
    assert data["spread_type"] == "single_card"
    assert data["question"] is None
    assert len(data["cards"]) == 1
    assert len(data["interpretation"]) > 50


def test_daily_reading_card_fields(client):
    response = client.post("/reading/daily")
    card = response.json()["cards"][0]
    assert "position" in card
    assert "name" in card
    assert card["orientation"] in ("Upright", "Reversed")
    assert isinstance(card["keywords"], list)
    assert len(card["meaning"]) > 0
    assert len(card["image_filename"]) > 0


def test_three_card_reading(client):
    response = client.post(
        "/reading/three-card",
        json={"question": "Should I pursue this new opportunity?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["spread_type"] == "three_card"
    assert data["question"] == "Should I pursue this new opportunity?"
    assert len(data["cards"]) == 3
    positions = [c["position"] for c in data["cards"]]
    assert positions == ["Past", "Present", "Future"]
    assert len(data["interpretation"]) > 100


def test_three_card_reading_requires_question(client):
    response = client.post("/reading/three-card", json={})
    assert response.status_code == 422


def test_celtic_cross_reading(client):
    response = client.post(
        "/reading/celtic-cross",
        json={"question": "How should I approach my career right now?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["spread_type"] == "celtic_cross"
    assert len(data["cards"]) == 10
    assert len(data["interpretation"]) > 200


def test_celtic_cross_reading_requires_question(client):
    response = client.post("/reading/celtic-cross", json={})
    assert response.status_code == 422


def test_cards_are_unique_within_reading(client):
    response = client.post(
        "/reading/celtic-cross",
        json={"question": "Will this relationship work out?"},
    )
    names = [c["name"] for c in response.json()["cards"]]
    assert len(names) == len(set(names)), "Duplicate cards in same reading"
