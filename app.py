
from flask import Flask, jsonify, render_template_string, request, redirect
from datetime import datetime, timezone

app = Flask(__name__)

SERVICES = [
    {"name": "Customer Portal", "code": "WEB", "status": "Operational",
     "uptime": "99.98%", "latency": "124 ms"},
    {"name": "Payments API", "code": "API", "status": "Degraded",
     "uptime": "99.91%", "latency": "482 ms"},
    {"name": "Authentication", "code": "AUTH", "status": "Operational",
     "uptime": "99.99%", "latency": "86 ms"},
    {"name": "Notification Service", "code": "MSG", "status": "Operational",
     "uptime": "99.95%", "latency": "163 ms"},
]

INCIDENTS = [
    {"id": "INC-1042", "service": "Payments API",
     "severity": "Critical", "status": "Investigating",
     "owner": "Platform Team"},
    {"id": "INC-1041", "service": "Customer Portal",
     "severity": "High", "status": "Monitoring",
     "owner": "Web Team"},
    {"id": "INC-1040", "service": "Notification Service",
     "severity": "Medium", "status": "Resolved",
     "owner": "Backend Team"},
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IncidentOps | Reliability Console</title>
<style>
:root {
 --bg:#0b1120; --panel:#111b2e; --line:#26344d;
 --text:#e7edf8; --muted:#8ea0bc; --blue:#8ba8ff;
 --green:#36d399; --amber:#fbbf24; --red:#fb7185;
}
* {box-sizing:border-box}
body {
 margin:0; background:var(--bg); color:var(--text);
 font:14px Arial, sans-serif;
}
.layout {display:grid; grid-template-columns:220px 1fr; min-height:100vh}
.sidebar {background:#0d1628; border-right:1px solid var(--line); padding:26px 16px}
.brand {font-size:20px; font-weight:bold; margin-bottom:42px}
.logo {display:inline-grid; place-items:center; background:#647fff;
 border-radius:9px; width:34px; height:34px; margin-right:9px}
.nav-label {font-size:10px; letter-spacing:2px; color:#657895; margin:25px 10px 12px}
.nav {padding:12px; border-radius:8px; color:var(--muted); margin:4px 0}
.nav.active {background:#1b2c4b; color:white}
.side-note {margin-top:45px; padding:14px; border:1px solid var(--line);
 border-radius:10px; color:var(--muted); line-height:1.8; font-size:12px}
main {padding:32px clamp(18px,4vw,52px); max-width:1500px; width:100%; margin:auto}
.top {display:flex; justify-content:space-between; align-items:center;
 flex-wrap:wrap; gap:15px; margin-bottom:28px}
.eyebrow {font-size:11px; color:var(--blue); letter-spacing:2px; text-transform:uppercase}
h1 {font-size:29px; margin:10px 0}
.subtitle {color:var(--muted); margin:0}
.live {border:1px solid #245643; color:#9af0ce; background:#102c27;
 border-radius:20px; padding:10px 14px}
.dot {display:inline-block; width:7px; height:7px; border-radius:50%;
 background:var(--green); margin-right:7px}
.metrics {display:grid; grid-template-columns:repeat(4,minmax(0,1fr));
 gap:15px; margin-bottom:18px}
.card {background:var(--panel); border:1px solid var(--line);
 border-radius:13px; padding:20px; min-width:0}
.metric-label {color:var(--muted); font-size:12px}
.metric {font-size:29px; font-weight:bold; margin:18px 0 8px}
.good {color:var(--green); font-size:11px}
.warn {color:var(--amber); font-size:11px}
.columns {display:grid; grid-template-columns:1.1fr .9fr; gap:17px; margin-bottom:18px}
.section-head {display:flex; justify-content:space-between; gap:10px;
 align-items:center; margin-bottom:14px}
h2 {font-size:15px; margin:0}
.small {font-size:11px; color:var(--muted)}
.service {display:flex; align-items:center; gap:12px; padding:15px 0;
 border-bottom:1px solid var(--line)}
.service:last-child {border-bottom:0}
.service-code {display:grid; place-items:center; width:38px; height:38px;
 border-radius:9px; background:#192742; color:var(--blue); font-weight:bold; font-size:11px}
.info {flex:1; min-width:0}
.service-name {font-weight:bold; margin-bottom:6px}
.right {text-align:right}
.status {display:inline-block; font-size:10px; padding:6px 8px; border-radius:6px}
.Operational {background:#10352e; color:#6ee7b7}
.Degraded {background:#3b2c13; color:#fcd34d}
.Resolved {background:#10352e; color:#6ee7b7}
.Investigating {background:#401d2b; color:#fda4af}
.Monitoring {background:#3b2c13; color:#fcd34d}
.incident {display:grid; grid-template-columns:82px 1fr auto;
 gap:10px; align-items:center; padding:15px 0; border-bottom:1px solid var(--line)}
.incident:last-child {border:0}
.inc-id {color:var(--blue); font-size:11px; font-weight:bold}
.severity {font-size:10px; font-weight:bold}
.Critical {color:var(--red)} .High {color:#fb923c} .Medium {color:var(--amber)}
form {display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:16px}
input, select {width:100%; min-width:0; padding:11px; color:var(--text);
 background:#0b1425; border:1px solid var(--line); border-radius:7px}
button {grid-column:1/-1; padding:12px; border:0; border-radius:7px;
 background:#8ba8ff; color:#0b1120; font-weight:bold; cursor:pointer}
button:hover {background:#b1c4ff}
.footer {padding:22px 2px; color:#657895; font-size:11px;
 display:flex; flex-wrap:wrap; justify-content:space-between; gap:10px}
@media(max-width:1000px) {
 .metrics {grid-template-columns:repeat(2,minmax(0,1fr))}
 .columns {grid-template-columns:1fr}
}
@media(max-width:650px) {
 .layout {grid-template-columns:1fr}
 .sidebar {display:none}
 main {padding:22px 14px}
 .metrics {gap:9px}
 .card {padding:14px}
 .metric {font-size:24px}
 .incident {grid-template-columns:75px 1fr}
 .incident>div:last-child {grid-column:2}
}
</style>
</head>
<body>
<div class="layout">
<aside class="sidebar">
 <div class="brand"><span class="logo">IO</span>IncidentOps</div>
 <div class="nav-label">WORKSPACE</div>
 <div class="nav active">▦ &nbsp; Overview</div>
 <div class="nav">◉ &nbsp; Service health</div>
 <div class="nav">⚑ &nbsp; Incidents</div>
 <div class="nav">⌁ &nbsp; Deployments</div>
 <div class="nav-label">MANAGEMENT</div>
 <div class="nav">◷ &nbsp; Activity log</div>
 <div class="nav">⚙ &nbsp; Settings</div>
 <div class="side-note"><b style="color:white">Environment</b><br>
 Production demo<br><span style="color:#36d399">●</span> Flask application</div>
</aside>
<main>
 <div class="top">
  <div><div class="eyebrow">Operations / Overview</div>
   <h1>Reliability Console</h1>
   <p class="subtitle">Monitor service health, incidents and platform performance.</p>
  </div>
  <div class="live"><span class="dot"></span>Platform status: demo</div>
 </div>

 <div class="metrics">
  <div class="card"><div class="metric-label">Services monitored</div>
   <div class="metric">04</div><div class="good">3 operational · 1 degraded</div></div>
  <div class="card"><div class="metric-label">Availability (30 days)</div>
   <div class="metric">99.95%</div><div class="good">Illustrative SLO metric</div></div>
  <div class="card"><div class="metric-label">Open incidents</div>
   <div class="metric">{{ open_count }}</div><div class="warn">Requires attention</div></div>
  <div class="card"><div class="metric-label">Median latency</div>
   <div class="metric">124 ms</div><div class="good">Illustrative demo metric</div></div>
 </div>

 <div class="columns">
  <section class="card">
   <div class="section-head"><h2>Service health</h2><span class="small">Current snapshot</span></div>
   {% for s in services %}
   <div class="service">
    <div class="service-code">{{ s.code }}</div>
    <div class="info"><div class="service-name">{{ s.name }}</div>
     <div class="small">30-day availability {{ s.uptime }}</div></div>
    <div class="right"><span class="status {{ s.status }}">{{ s.status }}</span>
     <div class="small" style="margin-top:7px">{{ s.latency }}</div></div>
   </div>
   {% endfor %}
  </section>

  <section class="card">
   <div class="section-head"><h2>Recent incidents</h2><span class="small">Latest activity</span></div>
   {% for i in incidents[:5] %}
   <div class="incident">
    <div class="inc-id">{{ i.id }}</div>
    <div><div class="service-name">{{ i.service }}</div>
     <div class="small">{{ i.status }} · {{ i.owner }}</div></div>
    <div class="severity {{ i.severity }}">{{ i.severity|upper }}</div>
   </div>
   {% endfor %}
  </section>
 </div>

 <div class="columns">
  <section class="card">
   <h2>Log an incident</h2>
   <p class="subtitle" style="margin-top:8px">Record an issue for the operations team.</p>
   <form method="post" action="/incidents">
    <input name="service" placeholder="Affected service" required>
    <input name="owner" placeholder="Responsible team" required>
    <select name="severity">
     <option>Low</option><option>Medium</option><option>High</option><option>Critical</option>
    </select>
    <select name="status">
     <option>Investigating</option><option>Monitoring</option><option>Resolved</option>
    </select>
    <button type="submit">+ Create incident</button>
   </form>
  </section>
  <section class="card">
   <div class="section-head"><h2>Deployment activity</h2><span class="small">CI/CD</span></div>
   <div class="service"><div class="service-code">CI</div><div class="info">
    <div class="service-name">Build and unit tests</div><div class="small">Jenkins pipeline</div>
   </div><span class="status Operational">Planned</span></div>
   <div class="service"><div class="service-code">CD</div><div class="info">
    <div class="service-name">Azure VM deployment</div><div class="small">Automated release</div>
   </div><span class="status Operational">Planned</span></div>
   <div class="service"><div class="service-code">IaC</div><div class="info">
    <div class="service-name">Infrastructure provisioning</div><div class="small">Terraform</div>
   </div><span class="status Operational">Planned</span></div>
  </section>
 </div>
 <div class="footer">
  <span>IncidentOps · DevOps IA3</span>
  <span>Metrics shown are illustrative, not live telemetry.</span>
  <span>Health endpoint: /health</span>
 </div>
</main>
</div>
</body>
</html>
"""


@app.get("/")
def dashboard():
    open_count = sum(1 for item in INCIDENTS if item["status"] != "Resolved")
    return render_template_string(
        HTML, services=SERVICES, incidents=INCIDENTS, open_count=open_count
    )


@app.post("/incidents")
def create_incident():
    service = request.form.get("service", "").strip()
    owner = request.form.get("owner", "").strip()
    severity = request.form.get("severity", "Medium")
    status = request.form.get("status", "Investigating")

    if service and owner:
        next_id = 1043 + len(INCIDENTS) - 3
        INCIDENTS.insert(0, {
            "id": f"INC-{next_id}",
            "service": service,
            "severity": severity,
            "status": status,
            "owner": owner,
        })

    return redirect("/")


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "app": "IncidentOps",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)