import Link from "next/link";

export default function NotFound() {
  return (
    <main className="min-h-screen bg-black flex flex-col items-center justify-center text-white">

      <h1 className="text-7xl font-bold">
        404
      </h1>

      <p className="mt-5 text-zinc-400">
        Page not found.
      </p>

      <Link
        href="/"
        className="mt-8 bg-red-600 px-6 py-3 rounded-xl"
      >
        Go Home
      </Link>

    </main>
  );
}