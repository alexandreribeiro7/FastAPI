from fastapi import FastAPI
from core.configs import settings
from core.api.v1.apy import api

app = FastAPI(
    title="Curso FastAPI - Segurança e Autenticação"
)

app.include_router(
    api,
    prefix=settings.API_V1_STR,
    tags=["API V1"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )

    """
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5NjgwNDYzLCJpYXQiOjE3NDkwNzU2NjMsInN1YiI6MX0.vHnSPRmR6EeKeCY8SEgxLP_-6Be7GXWgMrh4DkSsVxg"
    """