type MovieCardProps = {
  title: string;
  year: string;
  rating: string;
  genre: string;
};

export default function MovieCard({
  title,
  year,
  rating,
  genre,
}: MovieCardProps) {
  return (
    <div className="group overflow-hidden rounded-2xl border border-white/10 bg-zinc-900 transition duration-300 hover:-translate-y-2 hover:border-red-500">
      <div className="flex h-72 items-center justify-center bg-zinc-800 text-6xl">
        🎬
      </div>

      <div className="space-y-2 p-5">
        <h3 className="text-xl font-bold">{title}</h3>

        <div className="flex items-center justify-between text-sm text-gray-400">
          <span>{year}</span>
          <span>⭐ {rating}</span>
        </div>

        <span className="inline-block rounded-full bg-red-600/20 px-3 py-1 text-xs text-red-400">
          {genre}
        </span>
      </div>
    </div>
  );
}