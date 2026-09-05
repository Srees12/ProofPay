from typing import Any


CHECKLISTS = {
    "13.1_NON_RECEIPT": {"network": "Visa", "checks": ["proof_of_delivery", "delivery_timestamp", "recipient_confirmation"]},
    "10.4_FRAUD_CARD_ABSENT": {"network": "Visa / Mastercard", "checks": ["ip_match", "device_fingerprint", "authentication_history"]},
}


def inspect(reason_code: str, raw_evidence: dict[str, Any]) -> dict[str, Any]:
    checklist = CHECKLISTS.get(reason_code, {"network": "Visa / Mastercard", "checks": ["transaction_context", "fulfillment_records"]})
    tracking = raw_evidence["tracking"]
    access = raw_evidence["access"]
    matched = {
        "proof_of_delivery": bool(tracking.get("proof_of_delivery")),
        "delivery_timestamp": bool(tracking.get("events")),
        "recipient_confirmation": any(event.get("recipient") for event in tracking.get("events", [])),
        "ip_match": bool(access.get("ip_matched")),
        "device_fingerprint": bool(access.get("device_fingerprint")),
        "authentication_history": access.get("login_count", 0) > 0,
        "transaction_context": bool(raw_evidence["order"].get("order_id")),
        "fulfillment_records": bool(raw_evidence["order"].get("fulfillment_status")),
    }
    return {"network": checklist["network"], "required_checks": checklist["checks"], "matched_checks": matched}
