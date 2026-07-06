"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function SearchBar() {
  const router = useRouter();

  const [query, setQuery] = useState("");

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();

    if (!query.trim()) return;

    router.push(`/search?q=${encodeURIComponent(query)}`);
  }

  return (
    <form
      onSubmit={handleSearch}
      className="flex w-full max-w-2xl gap-3"
    >
      <input
        type="text"
        placeholder="Search movies..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 rounded-xl bg-zinc-900 px-5 py-4 outline-none border border-zinc-700 focus:border-red-500"
      />

      <button
        type="submit"
        className="rounded-xl bg-red-600 px-8 font-semibold hover:bg-red-700 transition"
      >
        Search
      </button>
    </form>
  );
}