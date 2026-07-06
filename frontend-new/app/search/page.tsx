import { searchMovies } from "@/lib/tmdb";
import MovieCard from "@/components/movie/MovieCard";
import SearchBar from "@/components/search/SearchBar";

type Props = {
  searchParams: Promise<{
    q?: string;
  }>;
};

export default async function SearchPage({
  searchParams,
}: Props) {
  const { q = "" } = await searchParams;

  const data = q
    ? await searchMovies(q)
    : { results: [] };

  const movies = data.results;

  return (
    <main className="min-h-screen bg-black text-white px-6 py-10">

      <div className="max-w-7xl mx-auto">

        <h1 className="text-5xl font-bold">
          Search Results
        </h1>

        <p className="text-zinc-400 mt-4">
          Showing <span className="text-white">{movies.length}</span> results for
        </p>

        <h2 className="text-3xl font-semibold mt-2 text-red-500">
          "{q}"
        </h2>
        <div className="mt-8">
         <SearchBar />
           </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mt-10">

          {movies.map((movie: any) => (
            <MovieCard
              key={movie.id}
              id={movie.id}
              title={movie.title}
              poster={movie.poster_path}
              rating={movie.vote_average}
            />
          ))}

        </div>

      </div>

    </main>
  );
}