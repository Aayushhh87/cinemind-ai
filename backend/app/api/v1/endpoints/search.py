from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.common import SemanticSearchRequest, SemanticSearchResponse
from app.services.search_service import semantic_search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/semantic", response_model=SemanticSearchResponse)
def search_semantic(
    payload: SemanticSearchRequest,
    db: Session = Depends(get_db),
) -> SemanticSearchResponse:
    results = semantic_search(db, payload.query, limit=payload.limit)
    return SemanticSearchResponse(query=payload.query, results=results)
