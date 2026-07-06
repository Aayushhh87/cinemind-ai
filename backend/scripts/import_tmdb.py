import urllib3
import certifi

urllib3.disable_warnings()
import os
import sys
import certifi
from datetime import datetime

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import requests
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.models import Movie

settings = get_settings()

API_KEY = settings.tmdb_api_key
BASE_URL = settings.tmdb_base_url


import time
import requests


def fetch_movies(page=1):
    url = f"{BASE_URL}/movie/top_rated"

    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params={
                    "api_key": API_KEY,
                    "page": page,
                    "language": "en-US",
                },
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json",
                    "Connection": "close",
                },
                timeout=60,
            )

            response.raise_for_status()
            return response.json()["results"]

        except Exception as e:
            print(f"Page {page} failed (try {attempt+1}/5): {e}")
            time.sleep(3)

    return []
    
    


def insert_movies(db: Session, movies):
    inserted = 0

    for m in movies:

        exists = (
            db.query(Movie)
            .filter(Movie.external_id == str(m["id"]))
            .first()
        )

        if exists:
            continue

        release_date = None

        if m.get("release_date"):
            try:
                release_date = datetime.strptime(
                    m["release_date"],
                    "%Y-%m-%d",
                ).date()
            except Exception:
                pass

        movie = Movie(
            title=m["title"],
            original_title=m.get("original_title"),
            overview=m.get("overview"),
            release_date=release_date,
            runtime_minutes=None,
            genres=[],
            director=None,
            cast_members=[],
            poster_url=(
                f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
                if m.get("poster_path")
                else None
            ),
            backdrop_url=(
                f"https://image.tmdb.org/t/p/original{m['backdrop_path']}"
                if m.get("backdrop_path")
                else None
            ),
            language=m.get("original_language"),
            vote_average=m.get("vote_average"),
            vote_count=m.get("vote_count"),
            popularity=m.get("popularity"),
            external_id=str(m["id"]),
            external_source="tmdb",
            embedding=None,
        )

        db.add(movie)
        inserted += 1

    db.commit()

    print(f"\n✅ Inserted {inserted} movies")


def main():
    db = SessionLocal()

    try:
        for page in range(1, 11):
            print(f"Downloading page {page}...")

            movies = fetch_movies(page)

            if movies:
                insert_movies(db, movies)
                print(f"Page {page} inserted.\n")

    finally:
        db.close()

        if __name__ == "__main__":
             main()

print("FILE LOADED")

if __name__ == "__main__":
    print("MAIN RUNNING")
    main()