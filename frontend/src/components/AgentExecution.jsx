import { Check, CircleDot, LoaderCircle } from 'lucide-react'

export default function AgentExecution({ audit }) {
  return <section className="panel execution-panel"><div className="panel-head"><div><span className="eyebrow">ORCHESTRATOR TRACE</span><h2>Agent execution</h2></div><span className="latency">{audit.processing_latency_ms} ms</span></div>
    <div className="trace">{audit.trace.map((step, index) => <div className="trace-row" key={`${step.action}-${index}`}><div className="trace-line"><span className={`trace-node ${step.status === 'failed' ? 'failed' : ''}`}>{step.status === 'completed' || step.status === 'AUTO_SUBMITTED' ? <Check size={13} /> : step.status === 'failed' ? '!' : <CircleDot size={13} />}</span>{index < audit.trace.length - 1 && <span className="connector" />}</div><div className="trace-copy"><div className="trace-title"><strong>{step.agent}</strong><span className={step.status === 'failed' ? 'text-danger' : 'text-muted'}>{step.status}</span></div><span className="mono action">{step.action}</span>{step.detail && <p>{step.detail}</p>}</div></div>)}</div>
    <div className="evidence-strip"><span>Evidence assembled</span><strong>{audit.decision.evidence_keys.length} keys</strong><span className="confidence-chip">{Math.round(audit.decision.win_confidence_score * 100)}% confidence</span></div>
  </section>
}
