from fastapi import APIRouter
from pydantic import BaseModel
from app.logger import log_event
from app.database import save_log

router = APIRouter()


BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "forget previous instructions",
    "forget all rules",
    "reveal system prompt",
    "show system prompt",
    "act as system",
    "bypass security",
    "disable safety",
    "jailbreak",
    "developer mode"
]


def detect_prompt_injection(prompt: str):

    prompt_lower = prompt.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in prompt_lower:
            return True

    return False

class PromptRequest(BaseModel):
    prompt: str

@router.post("/scan-prompt")
def scan_prompt(data: PromptRequest):

    prompt_lower = data.prompt.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in prompt_lower:
            log_event(f"Prompt Injection Detected: {pattern}")

            save_log(
                "PROMPT_INJECTION",
                f"Prompt Injection Detected: {pattern}"
            )

            return {
                "status": "blocked",
                "reason": pattern
            }