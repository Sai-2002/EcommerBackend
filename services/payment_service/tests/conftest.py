import sys
import os
from pathlib import Path

# Make `src` and `app` importable from within the payment_service directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Must be set before session.py is imported (create_engine runs at import time)
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost/testdb")
