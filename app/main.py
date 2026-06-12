from fastapi import FastAPI, Request, HTTPException

from app.services.logging_handler import AuditLogger

from app.auth import create_access_token, verify_token
from app.api_gateway import router as gateway_router
from app.prompt_filter import router as prompt_router
from app.response_filter import filter_response

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
    return {"status": "Gateway Running"}

@app.post("/v1/chat/completions")
async def process_gateway_request(request: Request):
    user_id = "user_test_123"
    user_prompt = "Hello AI, analyze this secure token."
    
    try:
        
        AuditLogger.log_incoming_request(user_id, user_prompt)
        
    
        if "malicious" in user_prompt.lower():
            raise ValueError("Insecure content detected in user prompt.")
            

        ai_response = "Response authorized by enterprise gateway."
        
    
        AuditLogger.log_outgoing_response(user_id, ai_response, status="CLEAN")
        return {"status": "success", "response": ai_response}
        
    except ValueError as val_err:
        
        error_msg = f"Validation Error: {str(val_err)}"
        AuditLogger.log_outgoing_response(user_id, error_msg, status="SUSPICIOUS")
        raise HTTPException(status_code=400, detail=error_msg)
        
    except Exception as e:
    
        error_msg = f"System Failure: {str(e)}"
        AuditLogger.log_outgoing_response(user_id, error_msg, status="BLOCKED")
        raise HTTPException(status_code=500, detail="Internal Security Gateway Error")
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

