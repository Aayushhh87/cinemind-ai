import Link from "next/link";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-black/80 backdrop-blur-md">
      <nav className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">

        {/* Logo */}

        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl">🎬</span>

          <h1 className="text-2xl font-bold tracking-wide text-red-500">
            CineMind
          </h1>
        </Link>

        {/* Navigation */}

        <div className="hidden lg:flex items-center gap-7 text-gray-300 text-sm">

          <Link href="/" className="hover:text-red-500 transition">
            Home
          </Link>

          <Link href="/dashboard" className="hover:text-red-500 transition">
            Dashboard
          </Link>

          <Link href="/favorites" className="hover:text-red-500 transition">
            Favorites
          </Link>

          <Link href="/watchlist" className="hover:text-red-500 transition">
            Watchlist
          </Link>

          <Link href="/recommendations" className="hover:text-red-500 transition">
            AI Picks
          </Link>

          <Link href="/chat" className="hover:text-red-500 transition">
            AI Chat
          </Link>

          <Link href="/profile" className="hover:text-red-500 transition">
            Profile
          </Link>

          <Link href="/settings" className="hover:text-red-500 transition">
            Settings
          </Link>

        </div>

        {/* Right Side */}

        <div className="flex items-center gap-3">

          <Link
            href="/chat"
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold hover:bg-blue-700 transition"
          >
            🤖 Ask AI
          </Link>

          <Link
            href="/profile"
            className="rounded-lg bg-zinc-800 px-4 py-2 text-sm font-semibold hover:bg-zinc-700 transition"
          >
            👤 Profile
          </Link>

        </div>

      </nav>
    </header>
  );
}