-- =====================================================================
-- CineMind AI — MVP Database Schema
-- PostgreSQL 14+
-- =====================================================================
-- Tables:
--   1. users   - app users / authentication
--   2. movies  - movie catalog
--   3. chats   - AI chat sessions + messages (linked to users & movies)
-- =====================================================================

-- Enable UUID generation (use gen_random_uuid(), built into pgcrypto)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Enable vector similarity search (pgvector)


-- =====================================================================
-- 1. USERS
-- =====================================================================
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    display_name    VARCHAR(100),
    avatar_url      TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_email ON users (email);

-- =====================================================================
-- 2. MOVIES
-- =====================================================================
CREATE TABLE movies (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title             VARCHAR(255) NOT NULL,
    original_title    VARCHAR(255),
    overview          TEXT,
    release_date      DATE,
    runtime_minutes   INTEGER CHECK (runtime_minutes IS NULL OR runtime_minutes > 0),
    genres            TEXT[] NOT NULL DEFAULT '{}',         -- e.g. {'Sci-Fi','Thriller'}
    director          VARCHAR(255),
    cast_members      TEXT[] NOT NULL DEFAULT '{}',
    poster_url        TEXT,
    backdrop_url      TEXT,
    language          VARCHAR(10) DEFAULT 'en',
    vote_average      NUMERIC(3,1) CHECK (vote_average IS NULL OR (vote_average >= 0 AND vote_average <= 10)),
    vote_count        INTEGER DEFAULT 0,
    popularity        NUMERIC(10,3) DEFAULT 0,
    external_id       VARCHAR(50),                          -- e.g. TMDb / IMDb id
    external_source   VARCHAR(20),                           -- e.g. 'tmdb', 'imdb'
    embedding         TEXT,                          -- requires pgvector; for AI semantic search
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (external_source, external_id)
);

CREATE INDEX idx_movies_title ON movies USING GIN (to_tsvector('english', title));
CREATE INDEX idx_movies_genres ON movies USING GIN (genres);
CREATE INDEX idx_movies_release_date ON movies (release_date);

-- =====================================================================
-- 3. CHATS
-- =====================================================================
-- A "chat" is one conversation session a user has with the AI.
CREATE TABLE chats (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(255),                            -- e.g. auto-generated chat title
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_chats_user_id ON chats (user_id);

-- Individual messages within a chat (user turns + AI turns).
CREATE TABLE chat_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id         UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    role            VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content         TEXT NOT NULL,
    recommended_movie_ids UUID[] DEFAULT '{}',                -- movies surfaced in this message
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_chat_messages_chat_id ON chat_messages (chat_id, created_at);

-- =====================================================================
-- Auto-update updated_at columns
-- =====================================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_movies_updated_at
    BEFORE UPDATE ON movies
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_chats_updated_at
    BEFORE UPDATE ON chats
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();