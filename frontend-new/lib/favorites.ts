export function getFavorites() {
  if (typeof window === "undefined") return [];

  const data = localStorage.getItem("favorites");

  return data ? JSON.parse(data) : [];
}

export function isFavorite(id: number) {
  return getFavorites().includes(id);
}

export function toggleFavorite(id: number) {
  const favorites = getFavorites();

  if (favorites.includes(id)) {
    const updated = favorites.filter((movieId: number) => movieId !== id);
    localStorage.setItem("favorites", JSON.stringify(updated));
    return false;
  }

  favorites.push(id);

  localStorage.setItem("favorites", JSON.stringify(favorites));

  return true;
}