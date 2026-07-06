"use client";

import { useEffect, useState } from "react";
import { isFavorite, toggleFavorite } from "@/lib/favorites";

type Props = {
  movieId: number;
};

export default function FavoriteButton({ movieId }: Props) {
  const [favorite, setFavorite] = useState(false);

  useEffect(() => {
    setFavorite(isFavorite(movieId));
  }, [movieId]);

  function handleClick() {
    const status = toggleFavorite(movieId);
    setFavorite(status);
  }

  return (
    <button
      onClick={handleClick}
      className={`px-6 py-3 rounded-xl transition ${
        favorite
          ? "bg-red-600 hover:bg-red-700"
          : "border border-zinc-600 hover:border-white"
      }`}
    >
      {favorite ? "❤️ Favorited" : "🤍 Add to Favorites"}
    </button>
  );
}