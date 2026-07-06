
import { fetchTrendingMovies } from "@/lib/tmdb";
import MovieCard from "@/components/movie/MovieCard";

export default async function TrendingMovies() {
  const { results: movies } = await fetchTrendingMovies();

  return (
    <section id="trending" className="py-20 px-6">
      <h2 className="text-3xl font-bold mb-8">
        🔥 Trending Movies
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
        {movies.slice(0, 10).map((movie: any) => (
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