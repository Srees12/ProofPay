from typing import Any


ORDERS: dict[str, dict[str, Any]] = {
    "txn_demo_001": {
        "order_id": "order_1001",
        "fulfillment_status": "delivered",
        "proof_of_delivery": True,
        "tracking_id": "SENTINEL-TRK-001",
        "delivered_at": "2026-09-02T10:34:00Z",
        "customer_email": "buyer@example.com",
    }
}


def get_order_details(transaction_id: str) -> dict[str, Any]:
    proof_of_delivery = "no-proof" not in transaction_id
    return ORDERS.get(
        transaction_id,
        {
            "order_id": f"order-{transaction_id}",
            "fulfillment_status": "fulfilled",
            "proof_of_delivery": proof_of_delivery,
            "tracking_id": f"TRK-{transaction_id[-6:].upper()}",
            "delivered_at": "2026-09-01T12:00:00Z",
            "customer_email": "customer@example.com",
        },
    )
