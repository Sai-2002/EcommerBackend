import os
import uuid
import jwt
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi.responses import Response

from app import app


def make_token(email: str = "user@example.com") -> str:
    return jwt.encode(
        {"user_id": str(uuid.uuid4()), "email": email},
        os.environ["JWT_SECRET"],
        algorithm="HS256",
    )


def upstream(status: int = 200, body: bytes = b'{"ok": true}') -> AsyncMock:
    return AsyncMock(
        return_value=Response(content=body, status_code=status, media_type="application/json")
    )


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


# ── Health ────────────────────────────────────────────────────────────────────

def test_health(client):
    assert client.get("/").json()["service"] == "api-gateway"


# ── Public routes — no token needed ──────────────────────────────────────────

def test_register_is_public(client):
    with patch("src.routes.gateway_router.forward_request", upstream()):
        r = client.post("/api/auth/register", json={"email": "a@b.com", "password": "pass1234"})
    assert r.status_code == 200


def test_login_is_public(client):
    with patch("src.routes.gateway_router.forward_request", upstream()):
        r = client.post("/api/auth/login", json={"email": "a@b.com", "password": "pass1234"})
    assert r.status_code == 200


def test_get_products_is_public(client):
    with patch("src.routes.gateway_router.forward_request", upstream(body=b"[]")):
        r = client.get("/api/products/")
    assert r.status_code == 200


def test_get_single_product_is_public(client):
    with patch("src.routes.gateway_router.forward_request", upstream()):
        r = client.get(f"/api/products/{uuid.uuid4()}")
    assert r.status_code == 200


def test_get_categories_is_public(client):
    with patch("src.routes.gateway_router.forward_request", upstream(body=b"[]")):
        r = client.get("/api/products/categories")
    assert r.status_code == 200


# ── Protected routes — missing token ─────────────────────────────────────────

@pytest.mark.parametrize("method,path", [
    ("POST",  "/api/orders/"),
    ("POST",  "/api/cart/"),
    ("POST",  "/api/payments/"),
    ("POST",  "/api/products/"),
    ("DELETE","/api/cart/items/some-id"),
])
def test_protected_route_no_token_returns_401(client, method, path):
    r = client.request(method, path, json={})
    assert r.status_code == 401


# ── Protected routes — bad token ─────────────────────────────────────────────

def test_invalid_token_returns_401(client):
    r = client.post(
        "/api/orders/", json={},
        headers={"Authorization": "Bearer not.a.real.token"},
    )
    assert r.status_code == 401


def test_wrong_scheme_returns_401(client):
    r = client.post(
        "/api/orders/", json={},
        headers={"Authorization": "Token sometoken"},
    )
    assert r.status_code == 401


# ── Protected routes — valid token ───────────────────────────────────────────

def test_valid_token_forwards_order(client):
    with patch("src.routes.gateway_router.forward_request", upstream()) as mock:
        r = client.post(
            "/api/orders/", json={},
            headers={"Authorization": f"Bearer {make_token()}"},
        )
    assert r.status_code == 200
    mock.assert_called_once()


def test_valid_token_forwards_cart(client):
    with patch("src.routes.gateway_router.forward_request", upstream()):
        r = client.post(
            "/api/cart/", json={},
            headers={"Authorization": f"Bearer {make_token()}"},
        )
    assert r.status_code == 200


def test_valid_token_forwards_payment(client):
    with patch("src.routes.gateway_router.forward_request", upstream()):
        r = client.post(
            "/api/payments/", json={},
            headers={"Authorization": f"Bearer {make_token()}"},
        )
    assert r.status_code == 200


def test_valid_token_forwards_create_product(client):
    with patch("src.routes.gateway_router.forward_request", upstream()):
        r = client.post(
            "/api/products/", json={},
            headers={"Authorization": f"Bearer {make_token()}"},
        )
    assert r.status_code == 200


# ── Routing ───────────────────────────────────────────────────────────────────

def test_unknown_service_returns_404(client):
    r = client.get(
        "/api/unknown/endpoint",
        headers={"Authorization": f"Bearer {make_token()}"},
    )
    assert r.status_code == 404


def test_upstream_error_is_passed_through(client):
    with patch("src.routes.gateway_router.forward_request", upstream(status=503)):
        r = client.get("/api/products/")
    assert r.status_code == 503
