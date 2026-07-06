import Link from "next/link";
import SearchBar from "@/components/search/SearchBar";

export default function Hero() {
  return (
    <section
      className="relative flex min-h-[90vh] items-center justify-center bg-cover bg-center"
      style={{
        backgroundImage:
          "url('https://image.tmdb.org/t/p/original/9nhjGaFLKtddDPtPaX5EmKqsWdH.jpg')",
      }}
    >
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/70" />

      {/* Content */}
      <div className="relative z-10 mx-auto max-w-5xl px-6 text-center">
        <h1 className="text-5xl font-extrabold leading-tight md:text-7xl">
          Discover Movies with
          <span className="block text-red-500">AI Intelligence</span>
        </h1>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-zinc-300">
          Search thousands of movies, get AI-powered recommendations,
          understand endings, and discover your next favorite film.
        </p>
        
        <div className="mt-10 flex justify-center">
  <SearchBar />
</div>
        <div className="mt-10 flex flex-wrap justify-center gap-5">
          <Link
            href="/chat"
            className="rounded-xl bg-red-600 px-8 py-4 font-semibold transition hover:bg-red-700"
          >
            🤖 Start AI Chat
          </Link>

          <a
            href="#trending"
            className="rounded-xl border border-zinc-600 px-8 py-4 transition hover:border-white"
          >
            🎬 Explore Movies
          </a>
        </div>

        <div className="mt-16 flex justify-center gap-12 text-center">
          <div>
            <h2 className="text-4xl font-bold text-red-500">10K+</h2>
            <p className="text-zinc-400">Movies</p>
          </div>

          <div>
            <h2 className="text-4xl font-bold text-red-500">AI</h2>
            <p className="text-zinc-400">Recommendations</p>
          </div>

          <div>
            <h2 className="text-4xl font-bold text-red-500">24/7</h2>
            <p className="text-zinc-400">Assistant</p>
          </div>
        </div>
      </div>
    </section>
  );
}