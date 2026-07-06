import MovieCard from "@/components/movie/MovieCard";

const favorites = [
  {
    id: 27205,
    title: "Inception",
    poster: "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    rating: 8.8,
  },
  {
    id: 155,
    title: "The Dark Knight",
    poster: "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    rating: 9.0,
  },
];

export default function FavoritesPage() {
  return (
    <main className="min-h-screen bg-black text-white px-6 py-10">
      <div className="max-w-7xl mx-auto">

        <h1 className="text-5xl font-bold">
          ❤️ My Favorites
        </h1>

        <p className="text-zinc-400 mt-3">
          Movies you've saved.
        </p>

        {favorites.length === 0 ? (
          <div className="mt-12 rounded-2xl bg-zinc-900 p-10 text-center">
            No favorites yet.
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mt-10">
            {favorites.map((movie) => (
              <MovieCard
                key={movie.id}
                id={movie.id}
                title={movie.title}
                poster={movie.poster}
                rating={movie.rating}
              />
            ))}
          </div>
        )}

      </div>
    </main>
  );
}