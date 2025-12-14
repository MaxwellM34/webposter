from pathlib import Path
from dotenv import load_dotenv
import os

# Load env vars from repo root .env (not required when hardcoding)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Hardcoded connection string to your pg-testing container on localhost:5432
DB_URL = "postgres://postgres:password@localhost:5432/testing"


class Config:
    TORTOISE_ORM = {
        "connections": {"default": "postgres://postgres:password@localhost:5432/testing"},
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            }
        },
    }

TORTOISE_ORM = Config.TORTOISE_ORM  # <- needed for Aerich
