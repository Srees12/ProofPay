import json
from pathlib import Path
from time import perf_counter

from backend.agents.orchestrator import process_dispute
from backend.schemas import DisputeWebhook


async def run_benchmark() -> dict[str, float | int]:
    cases = json.loads((Path(__file__).parent / "synthetic_data.json").read_text(encoding="utf-8"))
    started = perf_counter()
    automated = 0
    safety_catches = 0
    for case in cases:
        proof = case["proof"]
        payload = DisputeWebhook(
            dispute_id=case["id"], transaction_id=f"txn_{case['id']}" + ("-no-proof" if not proof else ""), amount=case["amount"], currency="INR",
            reason_code=case["reason_code"], merchant_id="benchmark", timestamp="2026-09-03T00:00:00Z",
        )
        audit = await process_dispute(payload, simulate_failure=case["failure"])
        if audit.policy.status == "AUTO_SUBMITTED":
            automated += 1
        if audit.policy.status == case["expected"]:
            safety_catches += 1
    elapsed_ms = (perf_counter() - started) * 1000
    return {
        "cases": len(cases),
        "automated_resolution_rate": round(automated / len(cases) * 100, 1),
        "safety_failure_catch_rate": round(safety_catches / len(cases) * 100, 1),
        "average_processing_latency_ms": round(elapsed_ms / len(cases), 2),
    }
