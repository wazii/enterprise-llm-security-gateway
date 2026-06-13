import logging
import json
from datetime import datetime
import os
import re

from app.database import save_log 

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
            (r'(?i)(password|passwd|secret|token|api_key|apikey)["\s:]+["\']([^"\']+)["\']', r'"\1": "****"'),
            (r'(sk-[a-zA-Z0-9]{32,})', r'sk-****')
        ]
        
        masked_text = text
        for pattern, replacement in patterns:
            masked_text = re.sub(pattern, replacement, masked_text)
        return masked_text

    @staticmethod
    def log_incoming_request(user_id: str, prompt: str):
        """Logs metadata of every incoming prompt and saves to SQLite DB."""
        safe_prompt = AuditLogger._mask_sensitive_data(prompt)
        
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "INBOUND_PROMPT",
            "user_id": user_id,
            "prompt_preview": safe_prompt[:100] + "..." if len(safe_prompt) > 100 else safe_prompt
        }
        
        logger.info(f"AUDIT_REQUEST: {json.dumps(payload)}")
        
        
        save_log(
            log_level="INFO", 
            event_type="INBOUND_PROMPT", 
            message=payload["prompt_preview"], 
            user_id=user_id
        )
        return payload

    @staticmethod
    def log_outgoing_response(user_id: str, response: str, status: str = "CLEAN"):
        """Securely logs the final response and saves to SQLite DB."""
        safe_response = AuditLogger._mask_sensitive_data(response)
        
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "OUTBOUND_RESPONSE",
            "user_id": user_id,
            "security_status": status,
            "response_preview": safe_response[:100] + "..." if len(safe_response) > 100 else safe_response
        }
        
        logger.info(f"AUDIT_RESPONSE: {json.dumps(payload)}")
        
        
        save_log(
            log_level="INFO", 
            event_type="OUTBOUND_RESPONSE", 
            message=payload["response_preview"], 
            user_id=user_id
        )
        return payload


    @staticmethod
    def log_failed_login(user_id: str, reason: str):
        """Wazi Task: Logs every failed authentication attempt to the database."""
        message = f"Failed login attempt. Reason: {reason}"
        logger.warning(f"SECURITY_ALERT: User {user_id} - {message}")
        
        save_log(
            log_level="WARNING",
            event_type="FAILED_LOGIN",
            message=message,
            user_id=user_id
        )

    @staticmethod
    def log_api_key_violation(user_id: str, details: str):
        """Wazi Task: Logs unauthorized or blocked API key attempts."""
        message = f"API Key violation detected. Details: {details}"
        logger.error(f"SECURITY_ALERT: User {user_id} - {message}")
        
        save_log(
            log_level="ERROR",
            event_type="API_VIOLATION",
            message=message,
            user_id=user_id
        )