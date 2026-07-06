#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Starting PostgreSQL and ChromaDB..."
docker compose up -d postgres chromadb

echo "Waiting for PostgreSQL..."
for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U cinemind -d cinemind >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

echo "Starting backend..."
docker compose up -d backend

echo "CineMind API: http://localhost:8000/docs"
