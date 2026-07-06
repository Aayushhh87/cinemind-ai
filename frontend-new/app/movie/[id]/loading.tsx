export default function Loading() {
  return (
    <div className="min-h-screen bg-black text-white animate-pulse">

      <div className="h-[500px] bg-zinc-800" />

      <div className="max-w-7xl mx-auto px-6 -mt-56 relative">

        <div className="flex gap-10">

          <div className="w-72 h-[420px] rounded-2xl bg-zinc-800" />

          <div className="flex-1 space-y-5">

            <div className="h-12 w-96 bg-zinc-800 rounded" />

            <div className="h-6 w-64 bg-zinc-800 rounded" />

            <div className="h-40 bg-zinc-800 rounded" />

          </div>

        </div>

      </div>

    </div>
  );
}