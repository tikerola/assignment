"""Runtime config loaded from `.env`"""
import os

from dotenv import load_dotenv

load_dotenv()


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable {name!r}.")
    return value


PASSWORD = _require("TEST_PASSWORD")
