import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.utils.error_handlers import register_exception_handlers
from src.api.views.auth import auth_router
from src.api.views.sleep_goals import sleep_goals_router
from src.api.views.sleep_notes import sleep_notes_router
from src.api.views.users import users_router
from src.core.config import settings


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sleep_goals_router)
app.include_router(sleep_notes_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host=settings.run.host, port=settings.run.port)
