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
# POST /cart/
# ---------------------------------------------------------------------------

def test_add_to_cart_new_item(client, mock_db):
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()
    item_id = uuid.uuid4()

    # find_by_user_and_product returns None (new item)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    # mock add/commit/refresh — refresh sets attributes on the db_item
    def mock_refresh(obj):
        obj.id = item_id
        obj.user_id = user_id
        obj.product_id = product_id
        obj.quantity = 1

    mock_db.refresh.side_effect = mock_refresh

    response = client.post("/cart/", json={
        "user_id": str(user_id),
        "product_id": str(product_id),
        "quantity": 1,
    })

    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 1


def test_add_to_cart_existing_item(client, mock_db):
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()
    item_id = uuid.uuid4()

    # find_by_user_and_product returns an existing item with quantity=2
    existing = MagicMock()
    existing.id = item_id
    existing.user_id = user_id
    existing.product_id = product_id
    existing.quantity = 2

    mock_db.query.return_value.filter.return_value.first.return_value = existing

    # update_quantity path — refresh returns updated mock
    updated = MagicMock()
    updated.id = item_id
    updated.user_id = user_id
    updated.product_id = product_id
    updated.quantity = 3

    mock_db.refresh.side_effect = lambda obj: setattr(obj, "quantity", 3)

    response = client.post("/cart/", json={
        "user_id": str(user_id),
        "product_id": str(product_id),
        "quantity": 1,
    })

    assert response.status_code == 200
    data = response.json()
    # quantity should be incremented (existing 2 + new 1 = 3)
    assert data["quantity"] == 3


def test_get_cart_success(client, mock_db):
    user_id = uuid.uuid4()

    # find_by_user_id returns empty list
    mock_db.query.return_value.filter.return_value.all.return_value = []

    response = client.get(f"/cart/{user_id}")

    assert response.status_code == 200
    assert response.json() == []


def test_update_cart_item_success(client, mock_db):
    item_id = uuid.uuid4()
    user_id = uuid.uuid4()
    product_id = uuid.uuid4()

    db_item = MagicMock()
    db_item.id = item_id
    db_item.user_id = user_id
    db_item.product_id = product_id
    db_item.quantity = 5

    mock_db.query.return_value.filter.return_value.first.return_value = db_item
    mock_db.refresh.side_effect = lambda obj: None

    response = client.put(f"/cart/items/{item_id}", json={"quantity": 5})

    assert response.status_code == 200


def test_update_cart_item_zero_quantity(client, mock_db):
    item_id = uuid.uuid4()

    response = client.put(f"/cart/items/{item_id}", json={"quantity": 0})

    assert response.status_code == 500


def test_remove_from_cart_success(client, mock_db):
    item_id = uuid.uuid4()

    mock_db.query.return_value.filter.return_value.delete.return_value = 1

    response = client.delete(f"/cart/items/{item_id}")

    assert response.status_code == 200


def test_clear_cart_success(client, mock_db):
    user_id = uuid.uuid4()

    mock_db.query.return_value.filter.return_value.delete.return_value = 1

    response = client.delete(f"/cart/{user_id}/clear")

    assert response.status_code == 200


def test_add_to_cart_missing_fields(client, mock_db):
    response = client.post("/cart/", json={})

    assert response.status_code == 422
