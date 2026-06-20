from app.database import save_log

def filter_response(response: str):

    blocked_keywords = [
        "password",
        "secret",
        "api_key",
        "token"
    ]

    for keyword in blocked_keywords:
        if keyword.lower() in response.lower():
            
            save_log(
                log_level="ERROR",
                event_type="DATA_LEAK_VIOLATION",
                message=f"Sensitive Data Leakage Detected in LLM Response! Blocked Keyword: '{keyword}'",
                user_id="system_filter"
            )

            return {
                "status": "blocked",
                "message": "Sensitive information detected and blocked by security gateway."
            }

    return {
        "status": "safe",
        "message": response
    }