"use client";

import { useState } from "react";
import Link from "next/link";
import { searchMovies } from "@/lib/tmdb";

export default function SearchSection() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);

      const data = await searchMovies(query);

      console.log(data);

      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      alert("Search failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-7xl px-6 py-20">
      <div className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl">

        <div className="mb-8 text-center">
          <h2 className="text-4xl font-bold">
            Search Movies with AI
          </h2>

          <p className="mt-3 text-gray-400">
            Ask naturally. CineMind understands what you mean.
          </p>
        </div>

        <div className="flex flex-col gap-4 md:flex-row">

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSearch();
            }}
            placeholder="Recommend sci-fi movies like Interstellar..."
            className="flex-1 rounded-xl border border-white/10 bg-black/40 px-5 py-4 outline-none focus:border-red-500"
          />

          <button
            onClick={handleSearch}
            disabled={loading}
            className="rounded-xl bg-red-600 px-8 py-4 font-semibold hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? "Searching..." : "🔍 Search"}
          </button>

        </div>

        <div className="mt-8 flex flex-wrap gap-3">

          {[
            "Marvel",
            "Christopher Nolan",
            "Oscar Winners",
            "Comedy",
            "Horror",
          ].map((item) => (
            <button
              key={item}
              onClick={() => setQuery(item)}
              className="rounded-full bg-white/5 px-4 py-2 text-sm hover:bg-red-600"
            >
              {item}
            </button>
          ))}

        </div>

      </div>

      {/* Results */}

      {results.length > 0 && (
        <div className="mt-16">

          <h2 className="mb-8 text-3xl font-bold">
            Search Results
          </h2>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">

            {results.map((movie: any) => (
           <Link
          key={movie.id}
         href={`/movie/${movie.id}`}
         className="overflow-hidden rounded-2xl bg-zinc-900 transition hover:scale-105"
          >
         <img
          src={
         movie.poster_path
          ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
          : "https://placehold.co/500x750?text=No+Poster"
         }
         alt={movie.title}
         className="h-[350px] w-full object-cover"
         />

         <div className="p-4">
         <h3 className="text-lg font-bold">
         {movie.title}
         </h3>

         <p className="mt-2 text-sm text-zinc-400">
         ⭐ {movie.vote_average?.toFixed(1)}
          </p>

         <p className="mt-3 text-sm text-zinc-500 line-clamp-3">
         {movie.overview}
         </p>
         </div>
         </Link>
          ))}
          </div>

        </div>
      )}

    </section>
  );
}