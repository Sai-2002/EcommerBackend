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
# POST /products/
# ---------------------------------------------------------------------------

def test_create_product_success(client, mock_db):
    product_id = uuid.uuid4()
    mock_product = MagicMock()
    mock_product.id = product_id
    mock_product.name = "Test Product"
    mock_product.description = "A test product"
    mock_product.price = 19.99
    mock_product.stock_quantity = 10
    mock_product.category_id = None
    mock_product.is_active = True

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda obj: setattr(obj, "id", product_id) or None

    # Make the refresh set the mock values we want returned
    def refresh_side_effect(obj):
        obj.id = product_id
        obj.name = "Test Product"
        obj.description = "A test product"
        obj.price = 19.99
        obj.stock_quantity = 10
        obj.category_id = None
        obj.is_active = True

    mock_db.refresh.side_effect = refresh_side_effect

    response = client.post("/products/", json={
        "name": "Test Product",
        "description": "A test product",
        "price": 19.99,
        "stock_quantity": 10
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"


def test_create_product_invalid_price(client, mock_db):
    response = client.post("/products/", json={
        "name": "Bad Product",
        "description": "A product with negative price",
        "price": -1,
        "stock_quantity": 10
    })

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# GET /products/{product_id}
# ---------------------------------------------------------------------------

def test_get_product_success(client, mock_db):
    product_id = uuid.uuid4()
    mock_product = MagicMock()
    mock_product.id = product_id
    mock_product.name = "Found Product"
    mock_product.description = "Found"
    mock_product.price = 9.99
    mock_product.stock_quantity = 5
    mock_product.category_id = None
    mock_product.is_active = True

    mock_db.query.return_value.filter.return_value.first.return_value = mock_product

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Found Product"


def test_get_product_not_found(client, mock_db):
    product_id = uuid.uuid4()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# GET /products/
# ---------------------------------------------------------------------------

def test_list_products_success(client, mock_db):
    mock_db.query.return_value.all.return_value = []

    response = client.get("/products/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


# ---------------------------------------------------------------------------
# PUT /products/{product_id}
# ---------------------------------------------------------------------------

def test_update_product_success(client, mock_db):
    product_id = uuid.uuid4()
    mock_product = MagicMock()
    mock_product.id = product_id
    mock_product.name = "Old Name"
    mock_product.description = "Old description"
    mock_product.price = 10.0
    mock_product.stock_quantity = 5
    mock_product.category_id = None
    mock_product.is_active = True

    updated_product = MagicMock()
    updated_product.id = product_id
    updated_product.name = "New Name"
    updated_product.description = "Old description"
    updated_product.price = 10.0
    updated_product.stock_quantity = 5
    updated_product.category_id = None
    updated_product.is_active = True

    # find_by_id returns existing, then find for update returns existing too
    mock_db.query.return_value.filter.return_value.first.return_value = mock_product
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = lambda obj: None

    response = client.put(f"/products/{product_id}", json={
        "name": "New Name"
    })

    assert response.status_code == 200


# ---------------------------------------------------------------------------
# DELETE /products/{product_id}
# ---------------------------------------------------------------------------

def test_delete_product_success(client, mock_db):
    product_id = uuid.uuid4()
    mock_db.query.return_value.filter.return_value.delete.return_value = 1
    mock_db.commit.return_value = None

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


# ---------------------------------------------------------------------------
# POST /products/categories
# ---------------------------------------------------------------------------

def test_create_category_success(client, mock_db):
    category_id = uuid.uuid4()

    def refresh_side_effect(obj):
        obj.id = category_id
        obj.name = "Electronics"
        obj.description = "Electronic products"

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = refresh_side_effect

    response = client.post("/products/categories", json={
        "name": "Electronics",
        "description": "Electronic products"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"


# ---------------------------------------------------------------------------
# GET /products/categories
# ---------------------------------------------------------------------------

def test_list_categories_success(client, mock_db):
    mock_db.query.return_value.all.return_value = []

    response = client.get("/products/categories")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
