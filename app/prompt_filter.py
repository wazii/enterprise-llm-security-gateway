from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "act as root",
    "bypass security",
    "developer mode"
]

class PromptRequest(BaseModel):
    prompt: str

@router.post("/scan-prompt")
def scan_prompt(data: PromptRequest):

    prompt_lower = data.prompt.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in prompt_lower:
            return {
                "status": "blocked",
                "reason": pattern
            }

    return {
        "status": "safe"
    }