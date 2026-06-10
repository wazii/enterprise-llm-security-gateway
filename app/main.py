from fastapi import FastAPI, Request, HTTPException

from app.services.logging_handler import AuditLogger

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
)

@app.get("/")
def home():
    return {"status": "Gateway Running"}

@app.post("/v1/chat/completions")
async def process_gateway_request(request: Request):
    user_id = "user_test_123"
    user_prompt = "Hello AI, analyze this secure token."
    
    try:
        
        AuditLogger.log_incoming_request(user_id, user_prompt)
        
    
        if "malicious" in user_prompt.lower():
            raise ValueError("Insecure content detected in user prompt.")
            

        ai_response = "Response authorized by enterprise gateway."
        
    
        AuditLogger.log_outgoing_response(user_id, ai_response, status="CLEAN")
        return {"status": "success", "response": ai_response}
        
    except ValueError as val_err:
        
        error_msg = f"Validation Error: {str(val_err)}"
        AuditLogger.log_outgoing_response(user_id, error_msg, status="SUSPICIOUS")
        raise HTTPException(status_code=400, detail=error_msg)
        
    except Exception as e:
    
        error_msg = f"System Failure: {str(e)}"
        AuditLogger.log_outgoing_response(user_id, error_msg, status="BLOCKED")
        raise HTTPException(status_code=500, detail="Internal Security Gateway Error")