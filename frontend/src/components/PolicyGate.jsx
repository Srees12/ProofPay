import { ShieldCheck, ShieldAlert } from 'lucide-react'

export default function PolicyGate({ audit }) {
  const approved = audit.policy.approved_for_auto_submit
  return <section className={`panel gate-panel ${approved ? 'gate-approved' : 'gate-escalated'}`}><div className="panel-head"><div><span className="eyebrow">IMMUTABLE CONTROL</span><h2>Policy gate</h2></div><span className="gate-icon">{approved ? <ShieldCheck size={21} /> : <ShieldAlert size={21} />}</span></div>
    <div className="gate-result"><span className="result-label">FINAL DISPOSITION</span><strong>{audit.policy.status.replaceAll('_', ' ')}</strong><p>{audit.policy.escalation_reason || 'All automated submission rules passed.'}</p></div>
    <div className="rule-list"><div className="rule"><span className="rule-mark">{audit.dispute.amount > 150000 ? '!' : '✓'}</span><span>Amount under INR 150,000</span><b>{audit.dispute.amount > 150000 ? 'TRIGGERED' : 'PASS'}</b></div><div className="rule"><span className="rule-mark">{audit.decision.win_confidence_score < .8 ? '!' : '✓'}</span><span>Confidence at least 80%</span><b>{audit.decision.win_confidence_score < .8 ? 'TRIGGERED' : 'PASS'}</b></div><div className="rule"><span className="rule-mark">{audit.evidence.proof_of_delivery || audit.dispute.reason_code !== '13.1_NON_RECEIPT' ? '✓' : '!'}</span><span>Delivery proof for non-receipt</span><b>{audit.evidence.proof_of_delivery || audit.dispute.reason_code !== '13.1_NON_RECEIPT' ? 'PASS' : 'TRIGGERED'}</b></div></div>
  </section>
}
