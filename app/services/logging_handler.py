# app/services/logging_handler.py
import logging
import json
from datetime import datetime

# Standard terminal logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Zaalima-Gateway-Logger")

class AuditLogger:
    @staticmethod
    def log_incoming_request(user_id: str, prompt: str):
        """AI Gateway par aane wale har prompt ka metadata console par log karega."""
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "INBOUND_PROMPT",
            "user_id": user_id,
            "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt
        }
        logger.info(f"AUDIT_REQUEST: {json.dumps(payload)}")
        return payload

    @staticmethod
    def log_outgoing_response(user_id: str, response: str, status: str = "CLEAN"):
        """LLM se aane wale final response ko securely log karega."""
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "OUTBOUND_RESPONSE",
            "user_id": user_id,
            "security_status": status,
            "response_preview": response[:100] + "..." if len(response) > 100 else response
        }
        logger.info(f"AUDIT_RESPONSE: {json.dumps(payload)}")
        return payload