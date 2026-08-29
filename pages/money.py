"""Shared price-string parsing for page objects."""

import re
from decimal import Decimal

_PRICE_RE = re.compile(r"\$(\d+\.\d{2})")


def parse_price(text: str) -> Decimal:
    """Extracts a dollar amount from text, e.g. "Item total: $58.97" -> Decimal("58.97")."""
    return Decimal(_PRICE_RE.search(text).group(1))
