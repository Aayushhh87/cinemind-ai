#!/usr/bin/env pwsh
# Start CineMind infrastructure and API

Set-Location $PSScriptRoot/..

Write-Host "Starting PostgreSQL and ChromaDB..."
docker compose up -d postgres chromadb

Write-Host "Waiting for PostgreSQL..."
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    docker compose exec -T postgres pg_isready -U cinemind -d cinemind 2>$null
    if ($LASTEXITCODE -eq 0) { $ready = $true; break }
    Start-Sleep -Seconds 2
}
if (-not $ready) { Write-Error "PostgreSQL did not become ready in time"; exit 1 }

Write-Host "Starting backend..."
docker compose up -d backend

Write-Host "CineMind API: http://localhost:8000/docs"
