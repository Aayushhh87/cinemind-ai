const movies = [
  "Interstellar",
  "The Dark Knight",
  "Inception",
  "Fight Club",
  "The Matrix",
  "Oppenheimer",
];

export default function RecommendationsPage() {
  return (
    <main className="min-h-screen bg-black text-white p-10">

      <h1 className="text-5xl font-bold mb-10">
        🤖 AI Recommendations
      </h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

        {movies.map((movie) => (
          <div
            key={movie}
            className="bg-zinc-900 rounded-2xl p-6 hover:bg-zinc-800 transition"
          >
            <h2 className="text-2xl font-bold">
              {movie}
            </h2>

            <p className="text-zinc-400 mt-3">
              Recommended based on your interests.
            </p>
          </div>
        ))}

      </div>

    </main>
  );
}