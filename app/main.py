from fastapi import FastAPI, Request
# Importing your custom AuditLogger from services
from app.services.logging_handler import AuditLogger

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
)

@app.get("/")
def home():
    return {"status": "Gateway Running"}

# New endpoint added for Day 3 Integration Task
@app.post("/v1/chat/completions")
async def process_gateway_request(request: Request):
    # Dummy data simulated for endpoint testing
    user_id = "user_test_123"
    user_prompt = "Hello AI, analyze this secure token."
    
    #  Trigger audit logging for the incoming request
    AuditLogger.log_incoming_request(user_id, user_prompt)
    
    # Simulating LLM response generation
    ai_response = "Response authorized by enterprise gateway."
    
    # Trigger audit logging for the outgoing response
    AuditLogger.log_outgoing_response(user_id, ai_response, status="CLEAN")
    
    return {"status": "success", "response": ai_response}