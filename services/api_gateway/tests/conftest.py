import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("AUTH_SERVICE_URL",    "http://auth-service:8001")
os.environ.setdefault("PRODUCT_SERVICE_URL", "http://product-service:8002")
os.environ.setdefault("ORDER_SERVICE_URL",   "http://order-service:8003")
os.environ.setdefault("CART_SERVICE_URL",    "http://cart-service:8004")
os.environ.setdefault("PAYMENT_SERVICE_URL", "http://payment-service:8005")
os.environ.setdefault("JWT_SECRET",          "test-secret-key-for-testing-32bytes!!")
