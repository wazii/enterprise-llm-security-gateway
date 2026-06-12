import logging
import json
from datetime import datetime
import os
import re


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app/services/security_audit.log", mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Zaalima-Gateway-Logger")

class AuditLogger:
    @staticmethod
    def _mask_sensitive_data(text: str) -> str:
        """Helper to mask common sensitive patterns like API keys, tokens, or passwords."""
        if not text:
            return text
        
        
        patterns = [
            (r'(?i)(password|passwd|secret|token|api_key|apikey)["\s:]+[\'"][^\'"]+[\'"]', r'\1: "****"'),
            (r'(sk-[a-zA-Z0-9]{32,})', r'sk-****') 
        ]
        
        masked_text = text
        for pattern, replacement in patterns:
            masked_text = re.sub(pattern, replacement, masked_text)
        return masked_text

    @staticmethod
    def log_incoming_request(user_id: str, prompt: str):
        """Logs metadata of every incoming prompt arriving at the AI Gateway with masking applied."""
        
        safe_prompt = AuditLogger._mask_sensitive_data(prompt)
        
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "INBOUND_PROMPT",
            "user_id": user_id,
            "prompt_preview": safe_prompt[:100] + "..." if len(safe_prompt) > 100 else safe_prompt
        }
        logger.info(f"AUDIT_REQUEST: {json.dumps(payload)}")
        return payload

    @staticmethod
    def log_outgoing_response(user_id: str, response: str, status: str = "CLEAN"):
        """Securely logs the final response received from the LLM with data masking."""
        safe_response = AuditLogger._mask_sensitive_data(response)
        
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "OUTBOUND_RESPONSE",
            "user_id": user_id,
            "security_status": status,
            "response_preview": safe_response[:100] + "..." if len(safe_response) > 100 else safe_response
        }
        logger.info(f"AUDIT_RESPONSE: {json.dumps(payload)}")
        return payload