"""Per-category hit counters for the recommendation service.

Added to answer "which catalog category are we recommending most" without a
real metrics backend — a plain in-process counter, incremented on every
`get_recommendations` call.
"""
from __future__ import annotations

import threading

_category_hits: dict[str, int] = {}
# Guards _category_hits: record_hit() is called concurrently from request
# threads, and its read-modify-write must be atomic to avoid lost updates.
_lock = threading.Lock()


def record_hit(category: str) -> None:
    """Increment the hit counter for `category`."""
    with _lock:
        current = _category_hits.get(category, 0)
        _category_hits[category] = current + 1


def hit_count(category: str) -> int:
    with _lock:
        return _category_hits.get(category, 0)


def total_hits() -> int:
    with _lock:
        return sum(_category_hits.values())
