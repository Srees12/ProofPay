from typing import Any


def get_access_logs(transaction_id: str) -> dict[str, Any]:
    return {
        "transaction_id": transaction_id,
        "ip_address": "103.21.244.10",
        "ip_matched": True,
        "login_count": 2,
        "last_login": "2026-09-02T10:20:00Z",
        "device_fingerprint": "fp_demo_7c21",
    }
