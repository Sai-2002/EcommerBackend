import uuid
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app import app
from src.infrastructure.session import get_db


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    yield TestClient(app, raise_server_exceptions=False)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# POST /orders/
# ---------------------------------------------------------------------------

def test_create_order_success(client, mock_db):
    saved_order = MagicMock()
    saved_order.id = uuid.uuid4()
    saved_order.user_id = uuid.uuid4()
    saved_order.status = "pending"
    saved_order.total_amount = 39.98

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda obj: None

    # Override refresh so saved_order is returned from save()
    def fake_refresh(obj):
        obj.id = saved_order.id
        obj.user_id = saved_order.user_id
        obj.status = saved_order.status
        obj.total_amount = saved_order.total_amount

    mock_db.refresh.side_effect = fake_refresh

    response = client.post("/orders/", json={
        "user_id": str(uuid.uuid4()),
        "items": [
            {"product_id": str(uuid.uuid4()), "quantity": 2, "unit_price": 19.99}
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert "status" in data
    assert data["status"] == "pending"


def test_create_order_empty_items(client, mock_db):
    saved_order = MagicMock()
    saved_order.id = uuid.uuid4()
    saved_order.user_id = uuid.uuid4()
    saved_order.status = "pending"
    saved_order.total_amount = 0.0

    def fake_refresh(obj):
        obj.id = saved_order.id
        obj.user_id = saved_order.user_id
        obj.status = saved_order.status
        obj.total_amount = saved_order.total_amount

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = fake_refresh

    response = client.post("/orders/", json={
        "user_id": str(uuid.uuid4()),
        "items": []
    })

    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["total_amount"] == 0.0


# ---------------------------------------------------------------------------
# GET /orders/{order_id}
# ---------------------------------------------------------------------------

def test_get_order_success(client, mock_db):
    order_id = uuid.uuid4()
    mock_order = MagicMock()
    mock_order.id = order_id
    mock_order.user_id = uuid.uuid4()
    mock_order.status = "pending"
    mock_order.total_amount = 29.99
    mock_order.created_at = None

    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == str(order_id)
    assert data["status"] == "pending"


def test_get_order_not_found(client, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get(f"/orders/{uuid.uuid4()}")

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# GET /orders/user/{user_id}
# ---------------------------------------------------------------------------

def test_list_user_orders_success(client, mock_db):
    mock_db.query.return_value.filter.return_value.all.return_value = []

    response = client.get(f"/orders/user/{uuid.uuid4()}")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


# ---------------------------------------------------------------------------
# PATCH /orders/{order_id}/status
# ---------------------------------------------------------------------------

def test_update_order_status_success(client, mock_db):
    order_id = uuid.uuid4()
    mock_order = MagicMock()
    mock_order.id = order_id
    mock_order.user_id = uuid.uuid4()
    mock_order.status = "confirmed"
    mock_order.total_amount = 49.99
    mock_order.created_at = None

    # find_by_id returns the mock order
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    # update_status: after commit/refresh, the order has updated status
    def fake_refresh(obj):
        obj.status = "confirmed"

    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = fake_refresh

    response = client.patch(f"/orders/{order_id}/status", json={"status": "confirmed"})

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"


def test_update_order_invalid_status(client, mock_db):
    order_id = uuid.uuid4()
    mock_order = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_order

    response = client.patch(f"/orders/{order_id}/status", json={"status": "invalid"})

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def test_missing_fields_returns_422(client, mock_db):
    response = client.post("/orders/", json={})

    assert response.status_code == 422
