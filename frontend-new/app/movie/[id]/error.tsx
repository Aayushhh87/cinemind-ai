"use client";

export default function Error() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center text-white">

      <div className="text-center">

        <h1 className="text-5xl font-bold">
          Something went wrong
        </h1>

        <p className="mt-5 text-zinc-400">
          Failed to load movie.
        </p>

      </div>

    </div>
  );
}