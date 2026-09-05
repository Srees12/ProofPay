import asyncio
from typing import Any


class CarrierTimeoutError(TimeoutError):
    pass


async def get_tracking_events(tracking_id: str, simulate_failure: bool = False) -> dict[str, Any]:
    await asyncio.sleep(0.05)
    if simulate_failure:
        raise CarrierTimeoutError("Shiprocket tracking API timed out")
    return {
        "tracking_id": tracking_id,
        "carrier": "Delhivery",
        "status": "DELIVERED",
        "proof_of_delivery": True,
        "events": [
            {"status": "PICKED_UP", "timestamp": "2026-08-30T08:15:00Z"},
            {"status": "OUT_FOR_DELIVERY", "timestamp": "2026-09-02T07:12:00Z"},
            {"status": "DELIVERED", "timestamp": "2026-09-02T10:34:00Z", "recipient": "Customer"},
        ],
    }
