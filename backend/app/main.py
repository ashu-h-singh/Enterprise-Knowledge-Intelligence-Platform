from fastapi import FastAPI
from backend.app.core.config import settings
from backend.app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "EKIP backend is running"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

app.include_router(router)
