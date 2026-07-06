import { fetchTrendingMovies } from "@/lib/tmdb";
import { Movie } from "@/types/movie";

export async function getTrendingMovies(): Promise<Movie[]> {
  const data = await fetchTrendingMovies();
  return data.results;
}