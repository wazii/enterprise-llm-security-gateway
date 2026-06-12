from fastapi import Header, HTTPException


def get_role(role: str = Header(...)):

    allowed_roles = [
        "admin",
        "security_analyst",
        "user"
    ]

    if role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail="Invalid role"
        )

    return role

from fastapi import Request
from fastapi.responses import JSONResponse

from app.auth import verify_token


async def auth_middleware(request: Request, call_next):

    protected_paths = [
        "/protected",
        "/admin-dashboard",
        "/analyst-dashboard"
    ]

    if request.url.path in protected_paths:

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Authorization header missing"
                }
            )

        token = auth_header.replace("Bearer ", "")

        verify_token(token)

    response = await call_next(request)

    return response

async def auth_middleware(request: Request, call_next):

    print("PATH:", request.url.path)
    print("HEADERS:", request.headers)

    response = await call_next(request)

    print("RESPONSE:", response)

    return response