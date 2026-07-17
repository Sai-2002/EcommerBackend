# 🛒 Ecommerce Backend

A production-ready **microservices backend** for an ecommerce platform, built with Python and FastAPI. Every service follows **Clean / Hexagonal Architecture** — business logic is completely decoupled from frameworks, databases, and transport.

---

## 📐 System Architecture

```
                        ┌─────────────────────────────────┐
                        │          API Gateway             │
                        │       FastAPI  :8000             │
                        │  ┌──────────────────────────┐   │
                        │  │  JWT Auth  │  httpx Proxy │   │
                        │  └──────────────────────────┘   │
                        └──────────────┬──────────────────┘
                                       │
              ┌──────────┬─────────────┼──────────────┬───────────┐
              │          │             │              │           │
      ┌───────▼──┐ ┌─────▼────┐ ┌─────▼────┐ ┌──────▼───┐ ┌─────▼────┐
      │   Auth   │ │ Product  │ │  Order   │ │   Cart   │ │ Payment  │
      │ Service  │ │ Service  │ │ Service  │ │ Service  │ │ Service  │
      │  :8001   │ │  :8002   │ │  :8003   │ │  :8004   │ │  :8005   │
      └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘
           │             │            │             │             │
      ┌────▼─────┐ ┌─────▼────┐ ┌────▼─────┐ ┌────▼─────┐ ┌────▼─────┐
      │ Postgres │ │ Postgres │ │ Postgres │ │ Postgres │ │ Postgres │
      │  auth_db │ │product_db│ │ order_db │ │  cart_db │ │payment_db│
      └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
```

All client traffic enters through the **API Gateway** on port `8000`. Public endpoints are forwarded directly; protected endpoints require a valid JWT that the gateway verifies before proxying.

---

## 🧱 Clean Architecture — Applied Consistently

Every service enforces the same four-layer structure. Dependencies only point inward — the domain layer has **zero external dependencies**.

```
┌─────────────────────────────────────────────────────┐
│  API Layer          routes · controllers · validators│  ← FastAPI, Pydantic
├─────────────────────────────────────────────────────┤
│  Application Layer       use cases                   │  ← Pure Python
├─────────────────────────────────────────────────────┤
│  Domain Layer      entities · repository interfaces  │  ← Pure Python, ABC
├─────────────────────────────────────────────────────┤
│  Infrastructure    ORM models · concrete repos       │  ← SQLAlchemy
└─────────────────────────────────────────────────────┘
```

| Layer | What lives here | What it depends on |
|---|---|---|
| **Domain** | `User`, `Product`, `Order`, … · `UserRepositoryInterface` | Nothing |
| **Application** | `RegisterUseCase`, `CreateOrderUseCase`, … | Domain only |
| **Infrastructure** | `UserRepository(UserRepositoryInterface)` · SQLAlchemy ORM models | Domain |
| **API** | FastAPI routes · Pydantic validators · controllers | Application + Infrastructure |

---

## 🗂️ Repository Structure

```
Backend/
├── pyproject.toml                  # Shared dependencies (uv)
└── services/
    ├── api_gateway/                # Single entry point — JWT auth + routing
    ├── auth_service/               # Registration & login — issues JWTs
    ├── product_service/            # Product & category catalogue
    ├── order_service/              # Order lifecycle management
    ├── cart_service/               # Per-user shopping cart
    └── payment_service/            # Payment record keeping
```

### Service layout (identical across all services)

```
<service>/
├── app.py                          # FastAPI app, router mount
├── .env / .env.example
└── src/
    ├── api/
    │   ├── routes/                 # APIRouter — register endpoints
    │   ├── controllers/            # Wire DB → repo → use case via Depends
    │   └── validators/             # Pydantic v2 request models
    ├── application/
    │   └── use_cases/              # One file per use case
    ├── domain/
    │   ├── entities/               # Pure Python domain objects
    │   └── interfaces/             # Abstract repository contracts (ABC)
    └── infrastructure/
        ├── session.py              # SQLAlchemy engine, sessionLocal, get_db()
        ├── model/                  # SQLAlchemy ORM models
        └── repository/             # Concrete repos — implement interfaces
└── tests/
    ├── conftest.py                 # sys.path + env setup, mock_db fixture
    └── test_<service>_routes.py    # pytest — TestClient + mocked DB session
```

---

## 🚀 Services & Endpoints

### 🔐 Auth Service — `:8001`

Handles user registration and login. Issues signed JWT tokens on success.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/register` | Public | Register a new user |
| `POST` | `/auth/login` | Public | Login and receive a JWT |

**Register**
```json
POST /auth/register
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Login**
```json
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### 📦 Product Service — `:8002`

Manages the product catalogue and categories.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/products/` | Public | List all products (optional `?category_id=`) |
| `GET` | `/products/{id}` | Public | Get a single product |
| `POST` | `/products/` | 🔒 JWT | Create a product |
| `PUT` | `/products/{id}` | 🔒 JWT | Update a product |
| `DELETE` | `/products/{id}` | 🔒 JWT | Delete a product |
| `GET` | `/products/categories` | Public | List all categories |
| `POST` | `/products/categories` | 🔒 JWT | Create a category |

**Create Product**
```json
POST /products/
{
  "name": "Wireless Headphones",
  "description": "Noise-cancelling over-ear headphones",
  "price": 149.99,
  "stock_quantity": 50,
  "category_id": "uuid-optional"
}
```

---

### 📋 Order Service — `:8003`

Manages the full order lifecycle from creation to delivery.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/orders/` | 🔒 JWT | Create a new order |
| `GET` | `/orders/{id}` | 🔒 JWT | Get order by ID |
| `GET` | `/orders/user/{user_id}` | 🔒 JWT | List all orders for a user |
| `PATCH` | `/orders/{id}/status` | 🔒 JWT | Update order status |

**Order statuses:** `pending` → `confirmed` → `shipped` → `delivered` (or `cancelled`)

**Create Order**
```json
POST /orders/
{
  "user_id": "uuid",
  "items": [
    { "product_id": "uuid", "quantity": 2, "unit_price": 149.99 }
  ]
}
```

---

### 🛒 Cart Service — `:8004`

Manages a per-user shopping cart. Adding an item that already exists increments quantity automatically.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/cart/` | 🔒 JWT | Add item to cart (increments if exists) |
| `GET` | `/cart/{user_id}` | 🔒 JWT | Get cart contents for a user |
| `PUT` | `/cart/items/{item_id}` | 🔒 JWT | Update item quantity |
| `DELETE` | `/cart/items/{item_id}` | 🔒 JWT | Remove a single item |
| `DELETE` | `/cart/{user_id}/clear` | 🔒 JWT | Clear entire cart |

---

### 💳 Payment Service — `:8005`

Creates and looks up payment records linked to orders. One payment per order is enforced.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/payments/` | 🔒 JWT | Create a payment for an order |
| `GET` | `/payments/{id}` | 🔒 JWT | Get payment by ID |
| `GET` | `/payments/order/{order_id}` | 🔒 JWT | Get payment by order |

**Payment methods:** `card` · `upi` · `wallet`

**Payment statuses:** `pending` · `completed` · `failed`

---

### 🌐 API Gateway — `:8000`

Single entry point. Verifies JWTs centrally and proxies requests to the correct downstream service.

```
POST  /api/auth/register          →  auth_service:8001       (public)
POST  /api/auth/login             →  auth_service:8001       (public)

GET   /api/products/              →  product_service:8002    (public)
GET   /api/products/{id}          →  product_service:8002    (public)
POST  /api/products/              →  product_service:8002    🔒 JWT
PUT   /api/products/{id}          →  product_service:8002    🔒 JWT
DELETE /api/products/{id}         →  product_service:8002    🔒 JWT

POST  /api/orders/                →  order_service:8003      🔒 JWT
GET   /api/orders/{id}            →  order_service:8003      🔒 JWT
GET   /api/orders/user/{user_id}  →  order_service:8003      🔒 JWT
PATCH /api/orders/{id}/status     →  order_service:8003      🔒 JWT

POST  /api/cart/                  →  cart_service:8004       🔒 JWT
GET   /api/cart/{user_id}         →  cart_service:8004       🔒 JWT
PUT   /api/cart/items/{id}        →  cart_service:8004       🔒 JWT
DELETE /api/cart/items/{id}       →  cart_service:8004       🔒 JWT
DELETE /api/cart/{user_id}/clear  →  cart_service:8004       🔒 JWT

POST  /api/payments/              →  payment_service:8005    🔒 JWT
GET   /api/payments/{id}          →  payment_service:8005    🔒 JWT
GET   /api/payments/order/{id}    →  payment_service:8005    🔒 JWT
```

---

## 🔑 Authentication Flow

```
Client                  Gateway               Auth Service
  │                        │                       │
  │── POST /api/auth/login ─►                       │
  │                        │── POST /auth/login ───►│
  │                        │◄── { access_token } ───│
  │◄── { access_token } ───│                        │
  │                        │                        │
  │── POST /api/orders/ ───►                        │
  │   Authorization:        │ verify JWT locally     │
  │   Bearer <token>        │ (no round-trip needed) │
  │                         │── POST /orders/ ──────►  order_service
  │◄── order response ──────│◄──────────────────────
```

The gateway verifies the JWT using the shared `JWT_SECRET` — **no round-trip to auth_service** on protected requests. Expired or tampered tokens are rejected at the perimeter with `401 Unauthorized`.

---

## ⚙️ Tech Stack

| Concern | Technology |
|---|---|
| Web framework | FastAPI 0.128+ |
| ORM | SQLAlchemy 2.x |
| Database | PostgreSQL (one instance per service) |
| Migrations | Alembic |
| Auth tokens | PyJWT + bcrypt |
| Request validation | Pydantic v2 |
| Gateway proxying | httpx (async) |
| Package manager | uv |
| Testing | pytest + FastAPI TestClient |
| Python | 3.9+ |

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) — `pip install uv`
- PostgreSQL running locally or via Docker

### 1. Install dependencies

```bash
git clone <repo-url>
cd ecommerce/Backend
uv sync --group dev
```

### 2. Configure environment variables

Each service reads its own `.env`. Copy and edit the examples:

```bash
for service in auth_service product_service order_service cart_service payment_service api_gateway; do
  cp services/$service/.env.example services/$service/.env
done
```

**Service `.env` (repeat for each, changing the DB name):**
```env
DATABASE_URL=postgresql://admin:password@localhost:5432/auth_db
JWT_SECRET=your-secret-key-minimum-32-characters-long
```

**Gateway `.env`:**
```env
AUTH_SERVICE_URL=http://localhost:8001
PRODUCT_SERVICE_URL=http://localhost:8002
ORDER_SERVICE_URL=http://localhost:8003
CART_SERVICE_URL=http://localhost:8004
PAYMENT_SERVICE_URL=http://localhost:8005
JWT_SECRET=your-secret-key-minimum-32-characters-long
```

> ⚠️ `JWT_SECRET` must be the **same value** in `auth_service/.env` and `api_gateway/.env`.

### 3. Run database migrations

```bash
cd services/auth_service
uv run alembic upgrade head
```

### 4. Start all services

```bash
# Each in its own terminal
cd services/auth_service    && uv run uvicorn app:app --port 8001 --reload
cd services/product_service && uv run uvicorn app:app --port 8002 --reload
cd services/order_service   && uv run uvicorn app:app --port 8003 --reload
cd services/cart_service    && uv run uvicorn app:app --port 8004 --reload
cd services/payment_service && uv run uvicorn app:app --port 8005 --reload
cd services/api_gateway     && uv run uvicorn app:app --port 8000 --reload
```

Interactive API docs are available at `http://localhost:<port>/docs` for every service.

---

## 🧪 Testing

All tests mock the SQLAlchemy session — **no database required** to run them.

```bash
# Run one service
cd services/auth_service && uv run pytest tests/ -v

# Run all services
for s in auth_service product_service order_service cart_service payment_service api_gateway; do
  echo "\n=== $s ===" && (cd services/$s && uv run pytest tests/ -v)
done
```

| Service | Tests | Result |
|---|---|---|
| api_gateway | 19 | ✅ |
| auth_service | 11 | ✅ |
| product_service | 9 | ✅ |
| order_service | 8 | ✅ |
| cart_service | 8 | ✅ |
| payment_service | 8 | ✅ |
| **Total** | **63** | **✅ all passing** |

---

## 🗃️ Domain Models

```
User                    Product                 Order
────────────────        ────────────────        ─────────────────────
id: UUID                id: UUID                id: UUID
email: str              name: str               user_id: UUID
password: str (hashed)  description: str        status: OrderStatus
isActive: bool          price: float            total_amount: float
                        stock_quantity: int      created_at: datetime
                        category_id: UUID?
                        is_active: bool          OrderItem
                                                 ─────────────────────
Category                CartItem                 id: UUID
────────────────        ────────────────         order_id: UUID
id: UUID                id: UUID                 product_id: UUID
name: str               user_id: UUID            quantity: int
description: str        product_id: UUID         unit_price: float
                        quantity: int
                                                Payment
                                                ─────────────────────
                                                id: UUID
                                                order_id: UUID
                                                user_id: UUID
                                                amount: float
                                                status: PaymentStatus
                                                payment_method: str
```

---

## 🏗️ Design Decisions

**Why Clean Architecture?**
Domain entities and use cases have no imports from FastAPI, SQLAlchemy, or any external library. Business logic is trivially unit-testable and the database or web framework can be swapped by only touching the infrastructure and API layers.

**Why one database per service?**
True data isolation — a schema migration in `product_db` cannot affect the order service. Each service is the sole owner of its data and can evolve independently.

**Why JWT verification at the gateway?**
Verifying the token once at the perimeter keeps individual services stateless and removes duplicated auth logic. A request that reaches a service has already been authenticated.

**Why httpx for proxying?**
`httpx` is async-native and integrates cleanly with FastAPI's async request handling, keeping the gateway non-blocking under concurrent load.

**Why uv?**
`uv` resolves and installs dependencies significantly faster than pip and provides a single `uv.lock` for reproducible builds.
