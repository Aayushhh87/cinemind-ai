import Link from "next/link";

export default function FeaturedBanner() {
  return (
    <section className="mx-auto max-w-7xl px-6">
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-red-700 via-red-900 to-black p-12 mb-12"></div>

      <div className="max-w-2xl">

        <p className="uppercase tracking-widest text-red-200 mb-3">
          Featured Movie
        </p>

        <h1 className="text-6xl font-black leading-tight">
          Oppenheimer
        </h1>

        <p className="mt-6 text-zinc-200 leading-8">
          Experience Christopher Nolan's masterpiece with stunning visuals,
          incredible performances and unforgettable storytelling.
        </p>

        <div className="mt-8 flex gap-4">

          <Link
            href="/movie/872585"
            className="bg-red-600 px-8 py-4 rounded-xl font-bold hover:bg-red-700"
          >
            ▶ Watch Details
          </Link>

          <button className="bg-white/10 px-8 py-4 rounded-xl hover:bg-white/20">
            ❤️ Add to Favorites
          </button>

        </div>

      </div>
    </section>
  );
}