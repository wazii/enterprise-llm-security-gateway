from fastapi import FastAPI, Header, HTTPException
from app.auth import create_access_token, verify_token
from app.api_gateway import router as gateway_router
from app.prompt_filter import router as prompt_router
from app.response_filter import filter_response

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
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

@app.post("/response-filter")
def test_response_filter(response: str):

    result = filter_response(response)

    return result