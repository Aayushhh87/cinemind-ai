import logging
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Movie
from app.services.embedding_service import generate_embedding, movie_document

logger = logging.getLogger(__name__)
_client: Any = None
_collection: Collection | None = None
_collection_unavailable = False


def get_chroma_client() -> Any:
    global _client, _collection_unavailable
    if _collection_unavailable:
        return None
    if _client is not None:
        return _client

    settings = get_settings()
    try:
        _client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
        _client.heartbeat()
        return _client
    except Exception:
        logger.warning("ChromaDB is not reachable at %s", settings.chroma_http_url)
        _collection_unavailable = True
        return None


def get_movies_collection() -> Collection | None:
    global _collection, _collection_unavailable
    if _collection_unavailable:
        return None
    if _collection is not None:
        return _collection

    client = get_chroma_client()
    if client is None:
        return None

    settings = get_settings()
    try:
        _collection = client.get_or_create_collection(name=settings.chroma_collection)
        return _collection
    except Exception:
        logger.exception("Failed to get or create ChromaDB collection")
        _collection_unavailable = True
        return None


def reset_collection() -> None:
    global _collection, _collection_unavailable, _client
    settings = get_settings()
    client = get_chroma_client()
    if client is None:
        return
    try:
        client.delete_collection(settings.chroma_collection)
    except Exception:
        pass
    _collection = client.get_or_create_collection(name=settings.chroma_collection)
    _collection_unavailable = False
