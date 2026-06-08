from fastapi import FastAPI, Header, HTTPException
from app.auth import create_access_token, verify_token

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
)

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

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/protected")
def protected_route(authorization: str = Header(...)):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    token = authorization.replace("Bearer ", "")

    payload = verify_token(token)

    return {
        "message": "Access Granted",
        "user": payload["sub"]
    }