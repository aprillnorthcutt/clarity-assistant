# config.py (create this once in your repo root)
import os
from dotenv import load_dotenv

# load .env automatically for local dev (no effect in Azure if not present)
load_dotenv()

def env(key: str, default: str | None = None, required: bool = False) -> str | None:
    val = os.getenv(key, default)
    if required and not val:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return val
