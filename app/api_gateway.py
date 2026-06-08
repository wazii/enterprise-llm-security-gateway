from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

VALID_API_KEYS = [
    "enterprise123",
    "test456"
]

class APIKeyRequest(BaseModel):
    api_key: str


@router.post("/validate-key")
def validate_key(data: APIKeyRequest):

    if data.api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return {
        "status": "valid",
        "message": "API Key Accepted"
    }