import uvicorn
from fastapi import FastAPI

from src.api.views.auth import auth_router
from src.core.config import settings


app = FastAPI()
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=settings.run.host, port=settings.run.port)
