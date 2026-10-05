"""
Kestrel Pay — Payment Processor (Demo Scaffold)

This module simulates payment authorization and retry logic.
No real payment processing occurs.
"""

import json
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Configuration (see gateway_config.py for details)
GATEWAY_TIMEOUT_SECONDS = 10
RETRY_ATTEMPTS = 3
RETRY_BACKOFF_MS = 500


class PaymentGatewayException(Exception):
    """Raised when payment gateway is unreachable or returns an error."""
    pass


def authorize_payment(
    merchant_id: str,
    amount_cents: int,
    currency: str = "USD",
    idempotency_key: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Authorize a payment transaction.

    Args:
        merchant_id: Merchant identifier (e.g., "MERCH-7412")
        amount_cents: Amount in cents (e.g., 12550 for $125.50)
        currency: ISO 4217 currency code (default: "USD")
        idempotency_key: Idempotency key for safe retries

    Returns:
        Dictionary with transaction details on success.

    Raises:
        PaymentGatewayException: If gateway is unreachable or times out.
    """
    if not idempotency_key:
        idempotency_key = str(uuid.uuid4())

    transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    print(f"[{timestamp}] Authorizing payment: {merchant_id} | {amount_cents/100:.2f} {currency}")
    print(f"  Idempotency key: {idempotency_key}")
    print(f"  Transaction ID: {transaction_id}")

    # Simulate gateway call with retry logic
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            print(f"  Attempt {attempt}/{RETRY_ATTEMPTS}...")
            response = _call_payment_gateway(
                merchant_id=merchant_id,
                amount_cents=amount_cents,
                currency=currency,
                transaction_id=transaction_id,
                idempotency_key=idempotency_key,
                timeout_seconds=GATEWAY_TIMEOUT_SECONDS,
            )
            print(f"  Result: SUCCESS")
            return response

        except PaymentGatewayException as e:
            print(f"  Result: {str(e)}")
            if attempt < RETRY_ATTEMPTS:
                backoff_seconds = (RETRY_BACKOFF_MS * (2 ** (attempt - 1))) / 1000
                print(f"  Retrying in {backoff_seconds:.1f}s...")
                time.sleep(backoff_seconds)
            else:
                print(f"  Retries exhausted. Failing transaction.")
                raise

    # Should not reach here
    raise PaymentGatewayException("Unexpected error during payment authorization")


def _call_payment_gateway(
    merchant_id: str,
    amount_cents: int,
    currency: str,
    transaction_id: str,
    idempotency_key: str,
    timeout_seconds: int,
) -> Dict[str, Any]:
    """
    Internal: Call the payment gateway (mocked).

    In production, this would make an HTTP request to the actual gateway.
    For this demo, we return a canned response.
    """
    # DEMO: Return success
    return {
        "transaction_id": transaction_id,
        "merchant_id": merchant_id,
        "amount_cents": amount_cents,
        "currency": currency,
        "status": "authorized",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "idempotency_key": idempotency_key,
    }


def main():
    """Demo: authorize a test transaction."""
    try:
        result = authorize_payment(
            merchant_id="MERCH-7412",
            amount_cents=12550,
            currency="USD",
        )
        print("\nAuthorization successful:")
        print(json.dumps(result, indent=2))
    except PaymentGatewayException as e:
        print(f"\nAuthorization failed: {e}")


if __name__ == "__main__":
    main()
