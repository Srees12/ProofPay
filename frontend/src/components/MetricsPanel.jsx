import { Activity, Gauge, Target } from 'lucide-react'

export default function MetricsPanel({ metrics, onRun }) {
  return <section className="panel metrics-panel"><div className="panel-head"><div><span className="eyebrow">SYNTHETIC EVAL</span><h2>Benchmark health</h2></div><button className="icon-button" title="Run evaluation" onClick={onRun}><Activity size={16} /></button></div><div className="metric-grid"><div><Gauge size={16} /><strong>{metrics.automated_resolution_rate ?? '--'}<small>%</small></strong><span>Auto resolution</span></div><div><Target size={16} /><strong>{metrics.safety_failure_catch_rate ?? '--'}<small>%</small></strong><span>Safety catch rate</span></div><div><Activity size={16} /><strong>{metrics.average_processing_latency_ms ?? '--'}<small>ms</small></strong><span>Avg latency</span></div></div><button className="run-button" onClick={onRun}>Run 20-case evaluation <span>↗</span></button></section>
}
