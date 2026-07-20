from fastapi import APIRouter, Request, Form
from fastapi.responses import (
    HTMLResponse,
    StreamingResponse,
    RedirectResponse
)

from app.database import (
    get_logs,
    get_all_logs,
    search_logs,
    filter_logs,
    get_total_events,
    get_event_count,
    get_event_by_id,
    update_investigation
)

import csv


import io

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    latest_event_id = None
    latest_event_type = None

    keyword = request.query_params.get("search", "").strip()
    event_filter = request.query_params.get("event_type", "").strip()

    if keyword:
        logs = search_logs(keyword)

    elif event_filter:
        logs = filter_logs(event_filter)

    else:
        logs = get_logs()

        latest_event_id = logs[0][0] if logs else 0
        latest_event_type = logs[0][1] if logs else "NO_EVENT"

    print("KEYWORD:", keyword)
    print("EVENT FILTER:", event_filter)
    print("LOG COUNT:", len(logs))
    print("LOGS:", logs)

    total_events = get_total_events()

    api_violations = get_event_count("API_KEY_VIOLATION")
    prompt_injections = get_event_count("PROMPT_INJECTION")
    pii_detections = get_event_count("PII_DETECTED")
    blocked_responses = get_event_count("RESPONSE_BLOCKED")

    risk_score = (
        api_violations
        + prompt_injections
        + pii_detections
        + blocked_responses
    )

    if risk_score < 5:
        risk_level = "🟢 LOW"
        risk_color = "#22c55e"

    elif risk_score < 10:
        risk_level = "🟠 MEDIUM"
        risk_color = "#fb923c"

    else:
        risk_level = "🔴 HIGH"
        risk_color = "#ef4444"

    html = f"""
<!DOCTYPE html>
<html>

<head>

<title>Enterprise LLM Security Dashboard</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body {{
    background:#0f172a;
    color:white;
    font-family:Arial, Helvetica, sans-serif;
    margin:40px;
}}

h1 {{
    color:#4ade80;
}}

h2 {{
    color:#38bdf8;
}}

.risk {{
    font-size:40px;
    font-weight:bold;
    color:{risk_color};
    margin-top:20px;
    margin-bottom:35px;
}}

.metric-container {{
    display:flex;
    flex-wrap:wrap;
    gap:25px;
    margin-bottom:40px;
}}

.card {{
    background:#1e293b;
    width:220px;
    border-radius:15px;
    padding:20px;
    box-shadow:0px 6px 15px rgba(0,0,0,.5);
}}

.card h3 {{
    color:#94a3b8;
    margin:0;
}}

.card h1 {{
    color:#4ade80;
    margin-top:15px;
}}

.charts {{
    display:flex;
    gap:30px;
    flex-wrap:wrap;
    margin-top:30px;
    margin-bottom:40px;
}}

.chart-box {{
    background:#1e293b;
    border-radius:15px;
    padding:20px;
}}

canvas {{
    width:500px !important;
    height:320px !important;
}}

table {{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}}

th {{
    background:#2563eb;
    padding:14px;
}}

td {{
    background:#1e293b;
    padding:12px;
}}

tr:hover td {{
    background:#334155;
}}

.alert-toast {{
    position: fixed;
    top: 25px;
    right: 25px;
    width: 340px;
    background: #1e293b;
    border-left: 6px solid #ef4444;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,.5);
    z-index: 9999;
    display: none;
    animation: slideIn 0.4s ease;
}}

.alert-toast h3 {{
    margin: 0 0 8px 0;
    color: #f87171;
}}

.alert-toast p {{
    margin: 0;
    color: #e2e8f0;
}}

@keyframes slideIn {{
    from {{
        transform: translateX(120%);
        opacity: 0;
    }}

    to {{
        transform: translateX(0);
        opacity: 1;
    }}
}}

</style>

</head>

<body>

<div id="alertToast" class="alert-toast">
    <h3>🚨 New Security Alert</h3>
    <p id="alertMessage">A new security event was detected.</p>
</div>

<h1>Enterprise LLM Security Dashboard</h1>

<div class="risk">
Current Risk Level : {risk_level}
</div>

<div class="metric-container">

<div class="card">
<h3>Total Events</h3>
<h1>{total_events}</h1>
</div>

<div class="card">
<h3>API Violations</h3>
<h1>{api_violations}</h1>
</div>

<div class="card">
<h3>Prompt Injections</h3>
<h1>{prompt_injections}</h1>
</div>

<div class="card">
<h3>PII Detections</h3>
<h1>{pii_detections}</h1>
</div>

<div class="card">
<h3>Blocked Responses</h3>
<h1>{blocked_responses}</h1>
</div>

</div>

<h2>Security Analytics</h2>

<div class="charts">

<div class="chart-box">
<canvas id="eventChart"></canvas>
</div>

<div class="chart-box">
<canvas id="riskChart"></canvas>
</div>

</div>

<h2>Recent Security Events</h2>

<form method="get" action="/dashboard" style="margin-bottom:20px;">

<input
type="text"
name="search"
placeholder="Search Events..."
value="{keyword}"
style="
padding:12px;
width:300px;
border-radius:8px;
border:none;
font-size:16px;
">

<button
style="
padding:12px 20px;
background:#2563eb;
color:white;
border:none;
border-radius:8px;
cursor:pointer;
">
Search
</button>

<a
href="/dashboard"
style="
margin-left:15px;
color:#4ade80;
text-decoration:none;
font-weight:bold;
">
Clear
</a>

</form>
<form method="get" style="margin-bottom:20px;">

<select
name="event_type"
style="
padding:10px;
border-radius:8px;
">

<option value="">All Events</option>

<option value="API_KEY_VIOLATION">
API Key Violations
</option>

<option value="PROMPT_INJECTION">
Prompt Injection
</option>

<option value="PII_DETECTED">
PII Detection
</option>

<option value="RESPONSE_BLOCKED">
Blocked Responses
</option>

</select>

<button
type="submit"
style="
padding:10px 18px;
background:#16a34a;
color:white;
border:none;
border-radius:8px;
cursor:pointer;
">
Filter
</button>

<a
href="/dashboard"
style="
margin-left:15px;
text-decoration:none;
color:#4ade80;
">
Reset
</a>

</form>
</form>

<div style="margin-bottom:20px;">

<a
href="/export-csv"
style="
background:#2563eb;
color:white;
padding:12px 20px;
text-decoration:none;
border-radius:8px;
font-weight:bold;
">

⬇ Export Audit Logs (CSV)

</a>

</div>

<table>
"""

    for log in logs:

        event_type = log[1]

        if event_type == "RESPONSE_BLOCKED":
            severity = """
            <span style="
            background:#dc2626;
            color:white;
            padding:6px 12px;
            border-radius:20px;
            font-weight:bold;
            ">
            🔴 Critical
            </span>
            """

        elif event_type == "PROMPT_INJECTION":
            severity = """
            <span style="
            background:#ea580c;
            color:white;
            padding:6px 12px;
            border-radius:20px;
            font-weight:bold;
            ">
            🟠 High
            </span>
            """

        elif event_type == "API_KEY_VIOLATION":
            severity = """
            <span style="
            background:#2563eb;
            color:white;
            padding:6px 12px;
            border-radius:20px;
            font-weight:bold;
            ">
            🔵 Medium
            </span>
            """

        elif event_type == "PII_DETECTED":
            severity = """
            <span style="
            background:#16a34a;
            color:white;
            padding:6px 12px;
            border-radius:20px;
            font-weight:bold;
            ">
            🟢 Low
            </span>
            """

        else:
            severity = """
            <span style="
            background:gray;
            color:white;
            padding:6px 12px;
            border-radius:20px;
            ">
            Unknown
            </span>
            """

        html += f"""
         <tr onclick="window.location.href='/event/{log[0]}'"
             style="cursor: pointer;">
    
             <td>{log[0]}</td>
             <td>{log[1]}</td>
             <td>{severity}</td>
             <td>{log[2]}</td>
             <td>{log[3]}</td>
    
         </tr>
         """

    html += f"""

</table>

<script>

new Chart(document.getElementById("eventChart"), {{

    type:"bar",

    data:{{

        labels:[
            "API",
            "Prompt",
            "PII",
            "Response"
        ],

        datasets:[{{

            label:"Security Events",

            data:[
                {api_violations},
                {prompt_injections},
                {pii_detections},
                {blocked_responses}
            ],

            backgroundColor:[
                "#3b82f6",
                "#f97316",
                "#22c55e",
                "#ef4444"
            ]

        }}]

    }}

}});

new Chart(document.getElementById("riskChart"), {{

    type:"pie",

    data:{{

        labels:[
            "API",
            "Prompt",
            "PII",
            "Response"
        ],

        datasets:[{{

            data:[
                {api_violations},
                {prompt_injections},
                {pii_detections},
                {blocked_responses}
            ],

            backgroundColor:[
                "#3b82f6",
                "#f97316",
                "#22c55e",
                "#ef4444"
            ]

        }}]

    }}

}});

// New Security Event Alert

const currentEventId = {latest_event_id};
const currentEventType = "{latest_event_type}";

const savedEventId = localStorage.getItem("lastSecurityEventId");

if (savedEventId === null) {{

    // First dashboard visit: remember the current event
    localStorage.setItem("lastSecurityEventId", currentEventId);

}} else if (currentEventId > Number(savedEventId)) {{

    const toast = document.getElementById("alertToast");
    const message = document.getElementById("alertMessage");

    message.textContent =
        currentEventType + " detected";

    toast.style.display = "block";

    localStorage.setItem("lastSecurityEventId", currentEventId);

    setTimeout(function() {{
        toast.style.display = "none";
    }}, 5000);

}}

// Auto Refresh Every 5 Seconds

setTimeout(function(){{
    location.reload();
}},5000);

</script>

</body>
</html>

"""

    return HTMLResponse(content=html)

@router.get("/export-csv")
def export_csv():

    logs = get_all_logs()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Event Type",
        "Event Message",
        "Timestamp"
    ])

    for log in logs:
        writer.writerow(log)

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=audit_logs.csv"
        }
    )

@router.get("/event/{event_id}", response_class=HTMLResponse)
def event_details(event_id: int):

    log = get_event_by_id(event_id)

    if log is None:
        return HTMLResponse(
            content="<h1>Security event not found</h1>",
            status_code=404
        )

    event_type = log[1]

    if event_type == "RESPONSE_BLOCKED":
        severity = "🔴 Critical"
        severity_color = "#dc2626"

    elif event_type == "PROMPT_INJECTION":
        severity = "🟠 High"
        severity_color = "#ea580c"

    elif event_type == "API_KEY_VIOLATION":
        severity = "🔵 Medium"
        severity_color = "#2563eb"

    elif event_type == "PII_DETECTED":
        severity = "🟢 Low"
        severity_color = "#16a34a"

    else:
        severity = "⚪ Unknown"
        severity_color = "#64748b"

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

    <title>Security Event #{log[0]}</title>

    <style>

    * {{
        box-sizing: border-box;
    }}

    body {{
        background: #0f172a;
        color: white;
        font-family: Arial, Helvetica, sans-serif;
        margin: 0;
        padding: 50px;
    }}

    .container {{
        max-width: 1000px;
        margin: auto;
    }}

    .back-button {{
        display: inline-block;
        color: #4ade80;
        text-decoration: none;
        font-weight: bold;
        margin-bottom: 30px;
    }}

    .back-button:hover {{
        color: #86efac;
    }}

    .header {{
        margin-bottom: 30px;
    }}

    .header h1 {{
        color: #38bdf8;
        font-size: 38px;
        margin-bottom: 10px;
    }}

    .header p {{
        color: #94a3b8;
        font-size: 18px;
    }}

    .event-card {{
        background: #1e293b;
        border-radius: 16px;
        padding: 35px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        border-left: 6px solid {severity_color};
    }}

    .event-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 30px;
    }}

    .event-id {{
        color: #94a3b8;
        font-size: 18px;
    }}

    .severity {{
        background: {severity_color};
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        font-weight: bold;
    }}

    .detail-row {{
        border-top: 1px solid #334155;
        padding: 22px 0;
    }}

    .label {{
        color: #94a3b8;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 8px;
        font-weight: bold;
    }}

    .value {{
        color: #f8fafc;
        font-size: 19px;
        line-height: 1.6;
        word-break: break-word;
    }}

    .status-box {{
        background: #0f172a;
        border-radius: 10px;
        padding: 20px;
        margin-top: 25px;
    }}

    .status-title {{
        color: #38bdf8;
        font-weight: bold;
        margin-bottom: 8px;
    }}

    .status-text {{
        color: #cbd5e1;
    }}

    </style>

    </head>

    <body>

    <div class="container">

        <a href="/dashboard" class="back-button">
            ← Back to Dashboard
        </a>

        <div class="header">

            <h1>Security Event Investigation</h1>

            <p>
                Detailed information for detected security event
            </p>

        </div>

        <div class="event-card">

            <div class="event-top">

                <div class="event-id">
                    Event ID: #{log[0]}
                </div>

                <div class="severity">
                    {severity}
                </div>

            </div>

            <div class="detail-row">

                <div class="label">
                    Event Type
                </div>

                <div class="value">
                    {log[1]}
                </div>

            </div>

            <div class="detail-row">

                <div class="label">
                    Security Message
                </div>

                <div class="value">
                    {log[2]}
                </div>

            </div>

            <div class="detail-row">

                <div class="label">
                    Detection Time
                </div>

                <div class="value">
                    {log[3]}
                </div>

            </div>

            <div class="status-box">

            <h3 style="color:#38bdf8;">
            Investigation Workflow
            </h3>
            
            <form
            action="/event/{log[0]}/update"
            method="post"
            >
            
            <label>Status</label>
            
            <br><br>
            
            <select
            name="status"
            style="
            width:100%;
            padding:12px;
            border-radius:8px;
            margin-bottom:20px;
            "
            >
            
            <option value="Open">Open</option>
            
            <option value="Investigating">
            Investigating
            </option>
            
            <option value="Resolved">
            Resolved
            </option>
            
            </select>
            
            <label>Analyst Notes</label>
            
            <br><br>
            
            <textarea
            name="analyst_notes"
            rows="6"
            style="
            width:100%;
            padding:12px;
            border-radius:8px;
            resize:vertical;
            "
            placeholder="Write investigation notes here..."
            ></textarea>
            
            <br><br>
            
            <button
            type="submit"
            style="
            background:#16a34a;
            color:white;
            padding:12px 22px;
            border:none;
            border-radius:8px;
            cursor:pointer;
            font-size:16px;
            "
            >
            
            💾 Save Investigation
            
            </button>
            
            </form>

</div>

        </div>

    </div>

    </body>

    </html>
    """

    return HTMLResponse(content=html)

@router.post("/event/{event_id}/update")
def save_investigation(
    event_id: int,
    status: str = Form(...),
    analyst_notes: str = Form("")
):

    allowed_statuses = [
        "Open",
        "Investigating",
        "Resolved"
    ]

    if status not in allowed_statuses:
        status = "Open"

    update_investigation(
        event_id,
        status,
        analyst_notes
    )

    return RedirectResponse(
        url=f"/event/{event_id}",
        status_code=303
    )