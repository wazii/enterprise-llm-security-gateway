from fastapi import FastAPI

app = FastAPI(
    title="Enterprise LLM Security Gateway",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "status": "Gateway Running"
    }