"""
Kestrel Pay — Payment Gateway Configuration

This module defines timeout, retry, and idempotency settings for payment processing.
"""

# Gateway timeout configuration
# Configure via Jira issue key tracking
GATEWAY_TIMEOUT_SECONDS = 5  # Timeout setting (demo value)
RETRY_ATTEMPTS = 3
RETRY_BACKOFF_MS = 500

# Idempotency settings
IDEMPOTENCY_CACHE_TTL_SECONDS = 3600  # 1 hour

# Service tier (for metric tracking)
SERVICE_TIER = "tier-1"

# Debug mode (disabled in production)
DEBUG = False

def get_timeout_config() -> dict:
    """Return current timeout configuration."""
    return {
        "gateway_timeout_seconds": GATEWAY_TIMEOUT_SECONDS,
        "retry_attempts": RETRY_ATTEMPTS,
        "retry_backoff_ms": RETRY_BACKOFF_MS,
        "idempotency_cache_ttl_seconds": IDEMPOTENCY_CACHE_TTL_SECONDS,
    }
