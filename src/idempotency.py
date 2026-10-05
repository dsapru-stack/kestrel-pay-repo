"""
Kestrel Pay — Idempotency Key Handling

This module ensures that payment authorization requests are safe to retry
by storing the result of each idempotency key.
"""

from typing import Dict, Optional, Any

# In-memory cache for demo purposes (no persistence)
_idempotency_cache: Dict[str, Any] = {}


def get_cached_result(idempotency_key: str) -> Optional[Any]:
    """
    Retrieve cached result for an idempotency key.
    
    Returns None if the key is not found or has expired.
    """
    return _idempotency_cache.get(idempotency_key)


def cache_result(idempotency_key: str, result: Any) -> None:
    """
    Cache the result of a payment authorization for the given idempotency key.
    
    In production, this would use Redis with TTL settings.
    For this demo, it uses in-memory storage.
    """
    _idempotency_cache[idempotency_key] = result


def clear_cache() -> None:
    """Clear the idempotency cache (for testing)."""
    _idempotency_cache.clear()
