"""Offline checks for the fictional Kestrel Pay demo scaffold."""
import pathlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import idempotency  # noqa: E402
import payment_processor  # noqa: E402


class MockAuthorizationTests(unittest.TestCase):
    def test_authorize_returns_canned_response_without_network(self):
        with patch.object(payment_processor, "_call_payment_gateway", wraps=payment_processor._call_payment_gateway) as gateway:
            result = payment_processor.authorize_payment("DEMO-MERCHANT", 500, idempotency_key="demo-key")
        self.assertEqual(result["status"], "authorized")
        self.assertEqual(result["amount_cents"], 500)
        self.assertEqual(result["idempotency_key"], "demo-key")
        gateway.assert_called_once()

    def test_gateway_failure_retries_at_most_configured_attempts(self):
        with patch.object(payment_processor, "_call_payment_gateway", side_effect=payment_processor.PaymentGatewayException("demo timeout")) as gateway, patch.object(payment_processor.time, "sleep") as sleep:
            with self.assertRaises(payment_processor.PaymentGatewayException):
                payment_processor.authorize_payment("DEMO-MERCHANT", 500, idempotency_key="demo-key")
        self.assertEqual(gateway.call_count, payment_processor.RETRY_ATTEMPTS)
        self.assertEqual(sleep.call_count, payment_processor.RETRY_ATTEMPTS - 1)
        self.assertEqual({call.kwargs["idempotency_key"] for call in gateway.call_args_list}, {"demo-key"})

    def test_in_memory_idempotency_helper(self):
        idempotency.clear_cache()
        self.assertIsNone(idempotency.get_cached_result("demo-key"))
        idempotency.cache_result("demo-key", {"result": "mock"})
        self.assertEqual(idempotency.get_cached_result("demo-key"), {"result": "mock"})
        idempotency.clear_cache()


if __name__ == "__main__":
    unittest.main()
