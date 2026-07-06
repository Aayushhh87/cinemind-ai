from fastapi import APIRouter

from app.api.v1.endpoints import chat, health, movies, search

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(movies.router)
api_router.include_router(search.router)
api_router.include_router(chat.router)
