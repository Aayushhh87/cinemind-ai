import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_TMDB_BASE_URL,
  timeout: 10000,
});

const API_KEY = process.env.NEXT_PUBLIC_TMDB_API_KEY!;
const BASE_URL = process.env.NEXT_PUBLIC_TMDB_BASE_URL!;

export async function fetchTrendingMovies() {
  try {
    const res = await api.get("/trending/all/day", {
      params: {
        api_key: API_KEY,
      },
    });

    console.log(res.data); // ye line add karo

    return {
      results: res.data.results.filter(
        (item: any) => item.media_type === "movie"
      ),
    };
  } catch (error) {
    console.error("TMDB Error:", error);

    return {
      results: [],
    };
  }
}



export async function fetchMovieDetails(id: string) {
  const res = await axios.get(
    `${BASE_URL}/movie/${id}`,
    {
      params: {
        api_key: API_KEY,
      },
    }
  );

  return res.data;
}

export async function searchMovies(query: string) {
  const res = await axios.get(
    `${BASE_URL}/search/movie`,
    {
      params: {
        api_key: API_KEY,
        query,
      },
    }
  );

  return res.data;
}

export async function fetchMovieVideos(id: string) {
  const res = await axios.get(
    `${BASE_URL}/movie/${id}/videos`,
    {
      params: {
        api_key: API_KEY,
      },
    }
  );

  return res.data;
}

export async function fetchSimilarMovies(id: string) {
  const res = await axios.get(
    `${BASE_URL}/movie/${id}/similar`,
    {
      params: {
        api_key: API_KEY,
      },
    }
  );

  return res.data;
}

export async function fetchTopRatedMovies() {
  try {
    const res = await api.get("/movie/top_rated", {
      params: {
        api_key: API_KEY,
      },
    });

    return res.data;
  } catch (error: any) {
    console.error("Top Rated Error:", error);

    return {
      results: [],
    };
  }
}