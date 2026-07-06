import Link from "next/link";
type MovieCardProps = {
    id: number;
  title: string;
  poster: string;
  rating: number;
};

export default function MovieCard({
    id,
  title,
  poster,
  rating,
}: MovieCardProps) {
  return (
  <Link href={`/movie/${id}`}>
    <div className="rounded-xl bg-zinc-900 overflow-hidden hover:scale-105 transition duration-300 cursor-pointer">
      <img
        src={
        poster
       ? `https://image.tmdb.org/t/p/w500${poster}`
       : "https://placehold.co/500x750/111111/FFFFFF?text=No+Poster"
          }
        alt={title}
        className="w-full h-72 object-cover"
      />

      <div className="p-4">
        <h3 className="font-semibold line-clamp-1">
          {title}
        </h3>

        <p className="text-sm text-zinc-400 mt-2">
          ⭐ {rating.toFixed(1)}
        </p>
      </div>
    </div>
  </Link>
);
}