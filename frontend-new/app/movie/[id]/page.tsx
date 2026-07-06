import RatingCircle from "@/components/movie/RatingCircle";
import FavoriteButton from "@/components/movie/FavoriteButton";
import Link from "next/link";
import MovieCard from "@/components/movie/MovieCard";
import {
  fetchMovieDetails,
  fetchMovieVideos,
  fetchSimilarMovies,
} from "@/lib/tmdb";

type Props = {
  params: Promise<{
    id: string;
  }>;
};

export default async function MoviePage({ params }: Props) {
  const { id } = await params;

  const movie = await fetchMovieDetails(id);

  const videos = await fetchMovieVideos(id);

  const similar = await fetchSimilarMovies(id);

  const trailer = videos.results.find(
    (v: any) => v.site === "YouTube" && v.type === "Trailer"
  );

  return (
    <main className="min-h-screen bg-black text-white">

      {/* Backdrop */}

      <div className="relative">

        <div className="flex flex-col items-center gap-6">

       <img
        src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
        alt={movie.title}
       className="w-72 rounded-2xl shadow-2xl"
        />

        <RatingCircle rating={movie.vote_average} />

       </div>

        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/30 to-transparent" />

      </div>

      {/* Movie Info */}

      <div className="max-w-7xl mx-auto px-6 -mt-56 relative z-10">

        <div className="flex flex-col lg:flex-row gap-10">

          {/* Poster */}

          <img
            src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
            alt={movie.title}
            className="w-72 rounded-2xl shadow-2xl"
          />

          {/* Details */}

          <div className="flex-1">

            <h1 className="text-5xl font-bold">
              {movie.title}
            </h1>

            <div className="flex flex-wrap gap-6 mt-6 text-zinc-300">

              <span>
                ⭐ {movie.vote_average.toFixed(1)}
              </span>

              <span>
                📅 {movie.release_date}
              </span>

              <span>
                ⏱ {movie.runtime} min
              </span>

              <span>
                🌍 {movie.original_language.toUpperCase()}
              </span>

            </div>

            <div className="flex flex-wrap gap-3 mt-6">

              {movie.genres.map((genre: any) => (

                <span
                  key={genre.id}
                  className="rounded-full bg-zinc-800 px-4 py-2"
                >
                  {genre.name}
                </span>

              ))}

            </div>

            <p className="mt-8 text-zinc-300 leading-8">
              {movie.overview}
            </p>

            {/* Buttons */}

            <div className="flex flex-wrap gap-4 mt-10">

              {trailer && (
                <a
                  href={`https://www.youtube.com/watch?v=${trailer.key}`}
                  target="_blank"
                  className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded-xl font-semibold"
                >
                  ▶ Watch Trailer
                </a>
              )}

              <FavoriteButton movieId={movie.id} />

              <Link
                href={`/chat?movie=${movie.title}`}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl"
              >
                🤖 Ask CineMind
              </Link>

            </div>

          </div>

        </div>

      </div> 

      {/* Similar Movies */}

      <section className="max-w-7xl mx-auto px-6 py-20">

        <div className="flex items-center justify-between mb-8">

          <h2 className="text-3xl font-bold">
            Similar Movies
          </h2>

          <Link
            href="/"
            className="text-red-500 hover:text-red-400"
          >
            ← Back Home
          </Link>

        </div>

        {similar.results.length > 0 ? (

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">

            {similar.results.slice(0, 10).map((item: any) => (

              <MovieCard
                key={item.id}
                id={item.id}
                title={item.title}
                poster={item.poster_path}
                rating={item.vote_average}
              />

            ))}

          </div>

        ) : (

          <div className="rounded-xl bg-zinc-900 p-8 text-center text-zinc-400">
            No similar movies found.
          </div>

        )}

      </section>

    </main>
  );
}