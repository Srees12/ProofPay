from backend.engine.policy_guardrail import DeterministicPolicyEngine


def test_high_value_escalates():
    result = DeterministicPolicyEngine().validate(150001, 0.99, True, "13.1_NON_RECEIPT")
    assert result.status == "ESCALATED_HUMAN_REVIEW"


def test_low_confidence_escalates():
    result = DeterministicPolicyEngine().validate(1000, 0.79, True, "10.4_FRAUD_CARD_ABSENT")
    assert result.status == "ESCALATED_HUMAN_REVIEW"


def test_non_receipt_without_delivery_is_rejected():
    result = DeterministicPolicyEngine().validate(1000, 0.99, False, "13.1_NON_RECEIPT")
    assert result.status == "REJECTED_INSUFFICIENT_EVIDENCE"


def test_complete_low_value_case_auto_submits():
    result = DeterministicPolicyEngine().validate(1000, 0.99, True, "13.1_NON_RECEIPT")
    assert result.approved_for_auto_submit is True
