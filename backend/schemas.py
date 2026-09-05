from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class DisputeWebhook(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dispute_id: str = Field(min_length=1)
    transaction_id: str = Field(min_length=1)
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    reason_code: str = Field(min_length=1)
    merchant_id: str = Field(min_length=1)
    timestamp: str


class EvidencePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proof_of_delivery: bool
    tracking_id: str
    ip_matched: bool
    access_log_timestamp: str
    raw_logs: dict[str, Any] = Field(default_factory=dict)


class AgentDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dispute_id: str
    win_confidence_score: float = Field(ge=0, le=1)
    evidence_keys: list[str]
    markdown_summary: str


class PolicyValidationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approved_for_auto_submit: bool
    status: Literal[
        "AUTO_SUBMITTED",
        "ESCALATED_HUMAN_REVIEW",
        "REJECTED_LOW_CONFIDENCE",
        "REJECTED_INSUFFICIENT_EVIDENCE",
    ]
    escalation_reason: str | None = None


class DisputeAudit(BaseModel):
    dispute: DisputeWebhook
    evidence: EvidencePayload
    decision: AgentDecision
    policy: PolicyValidationResult
    processing_latency_ms: float
    trace: list[dict[str, Any]]
    created_at: datetime = Field(default_factory=datetime.utcnow)
