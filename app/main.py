from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from app.auth import create_access_token, verify_token, create_refresh_token
from app.api_gateway import router as gateway_router
from app.prompt_filter import router as prompt_router
from app.response_filter import filter_response
from app.rbac import check_permission
from app.auth_middleware import get_role, auth_middleware
from starlette.middleware.base import BaseHTTPMiddleware


from app.database import save_log
from app.services.logging_handler import AuditLogger

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
)


@app.middleware("http")
async def db_system_error_logging_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        
        error_msg = f"Unhandled exception on {request.url.path}: {str(e)}"
        save_log(
            log_level="ERROR",
            event_type="SYSTEM_ERROR",
            message=error_msg,
            user_id="system"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error logged to system audit."}
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

    
    save_log(
        log_level="INFO",
        event_type="USER_LOGIN",
        message="User wazi logged in successfully",
        user_id="wazi"
    )

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

@app.get("/test-header")
def test_header(
    authorization: str = Header(None)
):
    return {
        "header": authorization
    }

@app.get("/test-log")
def test_log():
    
    save_log(
        log_level="INFO",
        event_type="TEST_EVENT",
        message="Test security event triggered via endpoint",
        user_id="test_user"
    )
    return {
        "message": "Log saved successfully to SQLite DB"
    }
