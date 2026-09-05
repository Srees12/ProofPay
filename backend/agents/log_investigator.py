from typing import Any

from backend.tools.access_logs_mock import get_access_logs
from backend.tools.shiprocket_mock import CarrierTimeoutError, get_tracking_events
from backend.tools.shopify_mock import get_order_details


async def investigate(transaction_id: str, simulate_failure: bool = False) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    trace: list[dict[str, Any]] = []
    order = get_order_details(transaction_id)
    trace.append({"agent": "Log Investigator", "action": "shopify.get_order_details", "status": "completed"})
    tracking: dict[str, Any]
    try:
        tracking = await get_tracking_events(order["tracking_id"], simulate_failure=simulate_failure)
        trace.append({"agent": "Log Investigator", "action": "shiprocket.get_tracking_events", "status": "completed"})
    except CarrierTimeoutError as error:
        tracking = {"status": "TIMEOUT", "proof_of_delivery": False, "events": [], "error": str(error)}
        trace.append({"agent": "Log Investigator", "action": "shiprocket.get_tracking_events", "status": "failed", "detail": str(error)})
    tracking["proof_of_delivery"] = bool(order.get("proof_of_delivery")) and bool(tracking.get("proof_of_delivery"))
    access = get_access_logs(transaction_id)
    trace.append({"agent": "Log Investigator", "action": "access_logs.get_auth_events", "status": "completed"})
    return {"order": order, "tracking": tracking, "access": access}, trace
