# CineMind AI — Backend (FastAPI)

MVP backend for CineMind AI: movie search + AI-powered chat recommendations.
Built to match the `cinemind_ai_schema.sql` schema (tables: `users`, `movies`, `chats`, `chat_messages`).

## Stack
- FastAPI + Uvicorn
- SQLAlchemy 2.0 (async) + asyncpg (PostgreSQL)
- Anthropic Python SDK (Claude) for the chat/recommendation logic
- Pydantic v2 for request/response validation

## Project layout
```
app/
  api/            # route handlers (movies, chats)
  core/           # settings/config
  db/             # SQLAlchemy engine + session
  models/         # ORM models (User, Movie, Chat, ChatMessage)
  schemas/        # Pydantic request/response models
  services/       # business logic (search, AI orchestration, chat persistence)
  main.py         # FastAPI app entrypoint
requirements.txt
.env.example
```

## Setup

1. **Create and activate a virtualenv:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # then edit .env: set DATABASE_URL and ANTHROPIC_API_KEY
   ```

4. **Set up the database.** Run the `cinemind_ai_schema.sql` file against your Postgres instance:
   ```bash
   psql "$DATABASE_URL_WITHOUT_ASYNC_DRIVER" -f cinemind_ai_schema.sql
   ```
   (Use a plain `postgresql://...` URL for `psql`, not the `postgresql+asyncpg://` one used by the app.)

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open the interactive docs:** http://localhost:8000/docs

## Endpoints

### `GET /movies/search`
Search the movie catalog.

Query params: `q` (text search), `genre` (exact genre filter), `limit`, `offset`.

```bash
curl "http://localhost:8000/movies/search?q=inception&limit=10"
```

### `POST /chats`
Send a message to CineMind AI. Creates a new chat if `chat_id` is omitted.

```bash
curl -X POST http://localhost:8000/chats \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "00000000-0000-0000-0000-000000000001",
    "message": "I want a mind-bending sci-fi movie like Inception"
  }'
```

Response includes the assistant's reply text, the `chat_id` (reuse this for follow-up
messages in the same conversation), and any `recommended_movies` pulled from the catalog.

### `GET /chats/{chat_id}`
Fetch full message history for a chat.

## Important MVP notes / what's intentionally simplified

- **No auth.** Endpoints take a raw `user_id` rather than verifying a JWT/session. You'll
  want to add real authentication (e.g. OAuth2 + JWT) before shipping this beyond a prototype.
- **No semantic/vector search yet.** The `movies` table in the SQL schema has an optional
  `embedding VECTOR(1536)` column for pgvector, but it's not used by this backend — search and
  AI candidate-selection both use simple keyword/`ILIKE` matching. Swap in pgvector + an
  embeddings pipeline later for real semantic search.
- **AI recommendation grounding.** The chat endpoint never lets Claude invent movies — it always
  picks from a candidate pool fetched from your actual `movies` table, returned by id. If your
  `movies` table is empty, the AI will just chat without recommendations.
- **No rate limiting / pagination cursors** — basic `limit`/`offset` only.

## Running tests / quick health check
```bash
curl http://localhost:8000/health
# {"status": "ok"}
```
