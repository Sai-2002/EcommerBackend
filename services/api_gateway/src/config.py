import os

SERVICE_REGISTRY: dict[str, str] = {
    "auth":     os.getenv("AUTH_SERVICE_URL"),
    "products": os.getenv("PRODUCT_SERVICE_URL"),
    "orders":   os.getenv("ORDER_SERVICE_URL"),
    "cart":     os.getenv("CART_SERVICE_URL"),
    "payments": os.getenv("PAYMENT_SERVICE_URL"),
}

# Exact (method, path) pairs that skip JWT verification
PUBLIC_ROUTES: set[tuple[str, str]] = {
    ("POST", "/api/auth/register"),
    ("POST", "/api/auth/login"),
}

# GET requests whose paths start with any of these prefixes are also public
PUBLIC_GET_PREFIXES: tuple[str, ...] = (
    "/api/products/",
    "/api/products",   # bare prefix without trailing slash
)
