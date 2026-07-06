from uuid import UUID

from chromadb.api.models.Collection import Collection
from sqlalchemy.orm import Session

from app.models import Movie
from app.services.embedding_service import generate_embedding, movie_document


def index_all_movies(db: Session, collection: Collection) -> int:
    movies = db.query(Movie).all()
    if not movies:
        return 0

    ids: list[str] = []
    documents: list[str] = []
    embeddings: list[list[float]] = []
    metadatas: list[dict] = []

    for movie in movies:
        document = movie_document(movie)
        vector = movie.embedding or generate_embedding(document)
        if movie.embedding is None:
            movie.embedding = vector
            db.add(movie)

        ids.append(str(movie.id))
        documents.append(document)
        embeddings.append(vector)
        metadatas.append(
            {
                "title": movie.title,
                "genres": ", ".join(movie.genres or []),
            }
        )

    db.commit()
    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
    return len(movies)


def query_movies(collection: Collection, query: str, limit: int = 10) -> list[tuple[UUID, float]]:
    vector = generate_embedding(query)
    result = collection.query(query_embeddings=[vector], n_results=limit)
    if not result["ids"] or not result["ids"][0]:
        return []

    distances = result["distances"][0] if result.get("distances") else [0.0] * len(result["ids"][0])
    output: list[tuple[UUID, float]] = []
    for movie_id, distance in zip(result["ids"][0], distances, strict=False):
        score = max(0.0, 1.0 - float(distance))
        output.append((UUID(movie_id), score))
    return output
