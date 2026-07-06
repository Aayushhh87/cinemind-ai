from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chats, movies
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="CineMind AI API",
    description="Backend for CineMind AI — movie search and AI chat-based recommendations.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(chats.router)


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}
