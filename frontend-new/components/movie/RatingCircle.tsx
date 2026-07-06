type Props = {
  rating: number;
};

export default function RatingCircle({ rating }: Props) {
  const percent = Math.round(rating * 10);

  let color = "text-red-500";

  if (percent >= 80) color = "text-green-500";
  else if (percent >= 60) color = "text-yellow-400";

  return (
    <div className="flex flex-col items-center">
      <div
        className={`w-20 h-20 rounded-full border-4 border-current ${color} flex items-center justify-center font-bold text-xl`}
      >
        {percent}%
      </div>

      <span className="text-sm text-zinc-400 mt-2">
        User Score
      </span>
    </div>
  );
}