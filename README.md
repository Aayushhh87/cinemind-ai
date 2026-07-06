# CineMind AI

Movie discovery platform with title search, semantic search, and AI chat.

## Quick start (Docker)

```bash
docker compose up -d --build
```

API docs: http://localhost:8000/docs

Health check: http://localhost:8000/api/v1/health

## Local backend (without Docker)

**Requirements:** Python 3.12+, PostgreSQL 16 with [pgvector](https://github.com/pgvector/pgvector), ChromaDB (optional)

1. Start PostgreSQL and apply schema:

```bash
psql -U cinemind -d cinemind -f database/schema.sql
psql -U cinemind -d cinemind -f database/seeds/movies.sql
```

2. Configure environment:

```bash
cp backend/.env.example backend/.env
```

3. Install and run:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/health` | Service health |
| GET | `/api/v1/movies?q=` | List or search movies |
| GET | `/api/v1/movies/{id}` | Movie details |
| POST | `/api/v1/search/semantic` | Natural language search |
| GET/POST | `/api/v1/chats` | Chat sessions (demo user) |
| POST | `/api/v1/chats/{id}/messages` | Send chat message |

Set `OPENAI_API_KEY` for richer AI chat and embeddings. Without it, the API uses deterministic mock embeddings and template responses.
