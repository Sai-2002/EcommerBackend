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
# POST /payments/
# ---------------------------------------------------------------------------

def test_create_payment_success(client, mock_db):
    order_id = uuid.uuid4()
    user_id = uuid.uuid4()
    payment_id = uuid.uuid4()

    # find_by_order_id returns None (no existing payment)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # refresh populates the ORM object returned from save
    def fake_refresh(obj):
        obj.id = payment_id
        obj.order_id = order_id
        obj.user_id = user_id
        obj.amount = 49.99
        obj.status = "pending"
        obj.payment_method = "card"

    mock_db.refresh.side_effect = fake_refresh

    response = client.post("/payments/", json={
        "order_id": str(order_id),
        "user_id": str(user_id),
        "amount": 49.99,
        "payment_method": "card",
    })

    assert response.status_code == 200
    data = response.json()
    assert "payment_id" in data
    assert data["amount"] == 49.99
    assert data["payment_method"] == "card"
    assert data["status"] == "pending"


def test_create_payment_duplicate_order(client, mock_db):
    order_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # find_by_order_id returns an existing payment mock
    existing = MagicMock()
    existing.id = uuid.uuid4()
    mock_db.query.return_value.filter.return_value.first.return_value = existing

    response = client.post("/payments/", json={
        "order_id": str(order_id),
        "user_id": str(user_id),
        "amount": 49.99,
        "payment_method": "card",
    })

    assert response.status_code == 500


def test_create_payment_invalid_amount(client, mock_db):
    order_id = uuid.uuid4()
    user_id = uuid.uuid4()

    # No existing payment
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.post("/payments/", json={
        "order_id": str(order_id),
        "user_id": str(user_id),
        "amount": 0,
        "payment_method": "card",
    })

    assert response.status_code == 500


def test_create_payment_missing_fields(client, mock_db):
    response = client.post("/payments/", json={})

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /payments/{payment_id}
# ---------------------------------------------------------------------------

def test_get_payment_success(client, mock_db):
    payment_id = uuid.uuid4()

    mock_payment = MagicMock()
    mock_payment.id = payment_id
    mock_payment.order_id = uuid.uuid4()
    mock_payment.user_id = uuid.uuid4()
    mock_payment.amount = 99.99
    mock_payment.status = "completed"
    mock_payment.payment_method = "upi"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_payment

    response = client.get(f"/payments/{payment_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["payment_id"] == str(payment_id)
    assert data["amount"] == 99.99


def test_get_payment_not_found(client, mock_db):
    payment_id = uuid.uuid4()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get(f"/payments/{payment_id}")

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# GET /payments/order/{order_id}
# ---------------------------------------------------------------------------

def test_get_payment_by_order_success(client, mock_db):
    order_id = uuid.uuid4()

    mock_payment = MagicMock()
    mock_payment.id = uuid.uuid4()
    mock_payment.order_id = order_id
    mock_payment.user_id = uuid.uuid4()
    mock_payment.amount = 150.00
    mock_payment.status = "pending"
    mock_payment.payment_method = "wallet"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_payment

    response = client.get(f"/payments/order/{order_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == str(order_id)
    assert data["amount"] == 150.00


def test_get_payment_by_order_not_found(client, mock_db):
    order_id = uuid.uuid4()

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get(f"/payments/order/{order_id}")

    assert response.status_code == 500
