# app/api_key_validator.py

from fastapi import Header, HTTPException
from app.logger import log_event
from app.database import save_log

VALID_API_KEYS = [
    "enterprise-key-123",
    "admin-key-456"
]


def validate_api_key(x_api_key: str = Header(None)):

    if not x_api_key:
        log_event("API Key Missing")

        save_log(
            "API_KEY_VIOLATION",
            "API Key Missing"
        )

        raise HTTPException(
            status_code=401,
            detail="API Key Required"
        )

    if x_api_key not in VALID_API_KEYS:

        log_event("Invalid API Key")

        save_log(
            "API_KEY_VIOLATION",
            f"Invalid API Key: {x_api_key}"
        )

        raise HTTPException(
            status_code=403,
            detail="Invalid API Key"
        )

    return True