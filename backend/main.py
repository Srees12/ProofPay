from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.orchestrator import process_dispute
from backend.config import settings
from backend.schemas import DisputeAudit, DisputeWebhook

app = FastAPI(title="ProofPay API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIT_LOG: list[DisputeAudit] = []


def demo_dispute(dispute_id: str, transaction_id: str, amount: float = 48_500, reason_code: str = "13.1_NON_RECEIPT") -> DisputeWebhook:
    return DisputeWebhook(
        dispute_id=dispute_id,
        transaction_id=transaction_id,
        amount=amount,
        currency="INR",
        reason_code=reason_code,
        merchant_id="merchant_demo_01",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "operational", "service": "proofpay"}


@app.post("/api/webhook/dispute", response_model=DisputeAudit)
async def dispute_webhook(payload: DisputeWebhook) -> DisputeAudit:
    audit = await process_dispute(payload)
    AUDIT_LOG.insert(0, audit)
    return audit


@app.post("/api/dispute/inject-chaos", response_model=DisputeAudit)
async def inject_chaos() -> DisputeAudit:
    payload = demo_dispute("dsp_chaos_001", "txn_chaos_001")
    audit = await process_dispute(payload, simulate_failure=True)
    AUDIT_LOG.insert(0, audit)
    return audit


@app.get("/api/disputes", response_model=list[DisputeAudit])
async def get_disputes() -> list[DisputeAudit]:
    return AUDIT_LOG


@app.post("/api/eval/run")
async def run_evaluation() -> dict[str, Any]:
    from backend.eval.benchmark import run_benchmark

    return await run_benchmark()


@app.on_event("startup")
async def seed_demo() -> None:
    if not AUDIT_LOG:
        AUDIT_LOG.append(await process_dispute(demo_dispute("dsp_demo_001", "txn_demo_001")))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
