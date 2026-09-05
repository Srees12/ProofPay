from typing import Any


def calculate_confidence(reason_code: str, evidence: dict[str, Any], inspection: dict[str, Any]) -> float:
    required = inspection["required_checks"]
    matched = inspection["matched_checks"]
    score = sum(bool(matched.get(key)) for key in required) / max(len(required), 1)
    if evidence["tracking"].get("status") == "TIMEOUT":
        score *= 0.55
    return round(min(score, 0.99), 2)


def synthesize(dispute_id: str, reason_code: str, evidence: dict[str, Any], inspection: dict[str, Any], confidence: float) -> str:
    order = evidence["order"]
    tracking = evidence["tracking"]
    access = evidence["access"]
    checks = inspection["matched_checks"]
    return f"""# Sentinel Evidence Brief: {dispute_id}

## Decision signal
- Reason code: `{reason_code}`
- Network checklist: {inspection['network']}
- Win confidence: **{confidence:.0%}**

## Fulfillment proof
- Order `{order['order_id']}` status: **{order['fulfillment_status']}**
- Tracking: `{order['tracking_id']}`
- Carrier status: **{tracking.get('status', 'UNKNOWN')}**
- Proof of delivery: **{'Verified' if checks.get('proof_of_delivery') else 'Unavailable'}**

## Customer and access corroboration
- IP matched: **{'Yes' if access.get('ip_matched') else 'No'}**
- Authentication events: **{access.get('login_count', 0)}**
- Device fingerprint: `{access.get('device_fingerprint', 'Unavailable')}`

## Evidence keys
`order_details`, `carrier_events`, `access_logs`, `network_checklist`
"""
