import uuid
import bcrypt
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
# POST /auth/register
# ---------------------------------------------------------------------------

def test_register_success(client, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "securepassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "user_id" in data
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email_returns_500(client, mock_db):
    existing = MagicMock()
    existing.email = "existing@example.com"
    mock_db.query.return_value.filter.return_value.first.return_value = existing

    response = client.post("/auth/register", json={
        "email": "existing@example.com",
        "password": "securepassword123"
    })

    assert response.status_code == 500


def test_register_invalid_email_returns_422(client, mock_db):
    response = client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "securepassword123"
    })

    assert response.status_code == 422


def test_register_missing_email_returns_422(client, mock_db):
    response = client.post("/auth/register", json={
        "password": "securepassword123"
    })

    assert response.status_code == 422


def test_register_missing_password_returns_422(client, mock_db):
    response = client.post("/auth/register", json={
        "email": "user@example.com"
    })

    assert response.status_code == 422


def test_register_empty_body_returns_422(client, mock_db):
    response = client.post("/auth/register", json={})

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------

def test_login_success(client, mock_db):
    hashed = bcrypt.hashpw(b"securepassword123", bcrypt.gensalt()).decode("utf-8")
    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_user.email = "user@example.com"
    mock_user.password = hashed
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    response = client.post("/auth/login", json={
        "email": "user@example.com",
        "password": "securepassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_not_found_returns_500(client, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.post("/auth/login", json={
        "email": "ghost@example.com",
        "password": "securepassword123"
    })

    assert response.status_code == 500


def test_login_wrong_password_returns_500(client, mock_db):
    hashed = bcrypt.hashpw(b"correctpassword", bcrypt.gensalt()).decode("utf-8")
    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_user.email = "user@example.com"
    mock_user.password = hashed
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    response = client.post("/auth/login", json={
        "email": "user@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 500


def test_login_invalid_email_returns_422(client, mock_db):
    response = client.post("/auth/login", json={
        "email": "not-an-email",
        "password": "securepassword123"
    })

    assert response.status_code == 422


def test_login_missing_fields_returns_422(client, mock_db):
    response = client.post("/auth/login", json={})

    assert response.status_code == 422
