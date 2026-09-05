from backend.config import settings
from backend.schemas import PolicyValidationResult


class DeterministicPolicyEngine:
    """Immutable, explainable policy gate. This class never calls an LLM."""

    def __init__(self, amount_limit_inr: float | None = None, minimum_confidence: float | None = None):
        self.amount_limit_inr = amount_limit_inr if amount_limit_inr is not None else settings.auto_submit_amount_limit_inr
        self.minimum_confidence = minimum_confidence if minimum_confidence is not None else settings.minimum_confidence

    def validate(
        self,
        dispute_amount: float,
        win_confidence_score: float,
        proof_of_delivery: bool,
        reason_code: str,
    ) -> PolicyValidationResult:
        if dispute_amount > self.amount_limit_inr:
            return PolicyValidationResult(
                approved_for_auto_submit=False,
                status="ESCALATED_HUMAN_REVIEW",
                escalation_reason="Amount exceeds automated threshold",
            )
        if not proof_of_delivery and reason_code == "13.1_NON_RECEIPT":
            return PolicyValidationResult(
                approved_for_auto_submit=False,
                status="REJECTED_INSUFFICIENT_EVIDENCE",
                escalation_reason="Proof of delivery is required for non-receipt disputes",
            )
        if win_confidence_score < self.minimum_confidence:
            return PolicyValidationResult(
                approved_for_auto_submit=False,
                status="ESCALATED_HUMAN_REVIEW",
                escalation_reason="Confidence below 80% safety margin",
            )
        return PolicyValidationResult(approved_for_auto_submit=True, status="AUTO_SUBMITTED")
