from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    return """
    <html>
        <head>
            <title>SOC Dashboard</title>
        </head>

        <body>
            <h1>Enterprise LLM Security Dashboard</h1>

            <h3>Security Metrics</h3>

            <ul>
                <li>Total Requests: 500</li>
                <li>Blocked Prompts: 15</li>
                <li>Failed Logins: 8</li>
                <li>Security Events: 22</li>
            </ul>
        </body>
    </html>
    """