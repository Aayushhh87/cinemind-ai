const watchlist = [
  "Avatar",
  "Batman Begins",
  "Dune",
  "John Wick",
  "Joker",
];

export default function WatchlistPage() {
  return (
    <main className="min-h-screen bg-black text-white p-10">

      <h1 className="text-5xl font-bold mb-10">
        🎬 Watchlist
      </h1>

      <div className="space-y-4">

        {watchlist.map((movie) => (
          <div
            key={movie}
            className="bg-zinc-900 rounded-xl p-5"
          >
            {movie}
          </div>
        ))}

      </div>

    </main>
  );
}