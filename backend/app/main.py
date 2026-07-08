import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.init_db import ensure_demo_user
from app.db.session import SessionLocal
from app.services.search_service import ensure_movie_embeddings, sync_movies_to_chroma

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging()
    settings = get_settings()
    logger.info("Starting %s (%s)", settings.app_name, settings.app_env)

    db = SessionLocal()
    try:
        ensure_demo_user(db)
        # embedded = ensure_movie_embeddings(db)
        # indexed = sync_movies_to_chroma(db)
        logger.info("Startup complete")

    except SQLAlchemyError:
        logger.exception("Database startup tasks failed — API will run in degraded mode")

    finally:
        db.close()

    yield


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://cinemind-ai-ten.vercel.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = create_app()