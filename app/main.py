from fastapi import FastAPI, Header, HTTPException, Depends
from app.auth import create_access_token, verify_token
from app.api_gateway import router as gateway_router
from app.prompt_filter import router as prompt_router
from app.response_filter import filter_response
from fastapi import Depends
from app.rbac import check_permission
from app.auth_middleware import get_role
from app.auth import create_refresh_token
from starlette.middleware.base import BaseHTTPMiddleware
from app.auth_middleware import auth_middleware
from app.logger import log_event
from app.database import save_log

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=auth_middleware
)

app.include_router(gateway_router)
app.include_router(prompt_router)


@app.get("/")
def home():
    return {
        "status": "Gateway Running"
    }

@app.post("/login")
def login():
    token = create_access_token(
        {"sub": "wazi"}
    )

    refresh_token = create_refresh_token(
        {"sub": "wazi"}
    )

    log_event("User logged in")
    save_log("User logged in")

    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.get("/protected")
def protected_route():

    return {
        "message": "Access Granted"
    }

@app.get("/admin-dashboard")
def admin_dashboard(role: str = Depends(get_role)):

    check_permission(
        role,
        "view_dashboard"
    )

    return {
        "message": "Admin Dashboard Access Granted",
        "role": role
    }


from fastapi import Request

@app.post("/refresh")
def refresh_token(
    request: Request,
    authorization: str = Header(None)
):

    print("AUTH =", authorization)
    print("HEADERS =", request.headers)

    return {
        "header": authorization
    }

from fastapi import Header

@app.get("/test-header")
def test_header(
    authorization: str = Header(None)
):
    return {
        "header": authorization
    }

@app.get("/test-log")
def test_log():

    log_event("Test security event")
    save_log("Test security event")

    return {
        "message": "Log saved successfully"
    }

