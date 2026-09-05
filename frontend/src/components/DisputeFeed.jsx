import { AlertTriangle, ChevronRight, Radio } from 'lucide-react'

export default function DisputeFeed({ disputes, selectedId, onSelect, onChaos, loading }) {
  return <section className="panel feed-panel">
    <div className="panel-head"><div><span className="eyebrow">INBOUND QUEUE</span><h2>Dispute feed</h2></div><Radio size={16} className="live-icon" /></div>
    <button className="chaos-button" onClick={onChaos} disabled={loading}><AlertTriangle size={15} />{loading ? 'Running...' : 'Inject API failure'}</button>
    <div className="feed-list">{disputes.map(item => <button className={`feed-item ${selectedId === item.dispute.dispute_id ? 'selected' : ''}`} key={item.dispute.dispute_id} onClick={() => onSelect(item)}>
      <div className="feed-top"><span className="mono">{item.dispute.dispute_id}</span><ChevronRight size={15} /></div>
      <strong>{item.dispute.reason_code.replaceAll('_', ' ')}</strong><div className="feed-meta"><span>{item.dispute.currency} {item.dispute.amount.toLocaleString()}</span><span className={`status-dot ${item.policy.approved_for_auto_submit ? 'green' : 'amber'}`} />{item.policy.status.replaceAll('_', ' ')}</div>
    </button>)}</div>
  </section>
}
