import MovieCard from "@/components/movie/MovieCard";
import { fetchTopRatedMovies } from "@/lib/tmdb";

export default async function TopRatedMovies() {
  const movies = await fetchTopRatedMovies();

  return (
    <section className="mx-auto max-w-7xl px-6 py-10">

      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-4xl font-bold">
          ⭐ Top Rated Movies
        </h2>

        <p className="text-zinc-400">
          Highest rated by TMDB users
        </p>
      </div>

      <div className="grid grid-cols-2 gap-6 md:grid-cols-3 lg:grid-cols-5">

        {movies.results.slice(0, 10).map((movie: any) => (
          <MovieCard
            key={movie.id}
            id={movie.id}
            title={movie.title}
            poster={movie.poster_path}
            rating={movie.vote_average}
          />
        ))}

      </div>

    </section>
  );
}