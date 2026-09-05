from time import perf_counter
from typing import Any

from backend.agents.evidence_synthesizer import calculate_confidence, synthesize
from backend.agents.log_investigator import investigate
from backend.agents.policy_inspector import inspect
from backend.engine.policy_guardrail import DeterministicPolicyEngine
from backend.schemas import AgentDecision, DisputeAudit, DisputeWebhook, EvidencePayload


async def process_dispute(dispute: DisputeWebhook, simulate_failure: bool = False) -> DisputeAudit:
    started = perf_counter()
    raw_evidence, trace = await investigate(dispute.transaction_id, simulate_failure)
    trace.append({"agent": "Policy Inspector", "action": "match_network_reason_code", "status": "completed"})
    inspection = inspect(dispute.reason_code, raw_evidence)
    confidence = calculate_confidence(dispute.reason_code, raw_evidence, inspection)
    summary = synthesize(dispute.dispute_id, dispute.reason_code, raw_evidence, inspection, confidence)
    trace.append({"agent": "Evidence Synthesizer", "action": "generate_markdown_brief", "status": "completed"})
    order = raw_evidence["order"]
    tracking = raw_evidence["tracking"]
    access = raw_evidence["access"]
    evidence = EvidencePayload(
        proof_of_delivery=bool(tracking.get("proof_of_delivery", False)),
        tracking_id=order["tracking_id"],
        ip_matched=bool(access.get("ip_matched", False)),
        access_log_timestamp=access.get("last_login", ""),
        raw_logs=raw_evidence,
    )
    decision = AgentDecision(
        dispute_id=dispute.dispute_id,
        win_confidence_score=confidence,
        evidence_keys=["order_details", "carrier_events", "access_logs", "network_checklist"],
        markdown_summary=summary,
    )
    policy = DeterministicPolicyEngine().validate(dispute.amount, confidence, evidence.proof_of_delivery, dispute.reason_code)
    trace.append({"agent": "Deterministic Policy Gate", "action": "validate_submission", "status": policy.status, "reason": policy.escalation_reason})
    return DisputeAudit(dispute=dispute, evidence=evidence, decision=decision, policy=policy, processing_latency_ms=round((perf_counter() - started) * 1000, 2), trace=trace)
