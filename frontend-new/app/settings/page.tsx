export default function SettingsPage() {
  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-5xl font-bold mb-10">
        ⚙️ Settings
      </h1>

      <div className="max-w-2xl space-y-6">

        <div className="bg-zinc-900 rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-2">
            Theme
          </h2>

          <p className="text-zinc-400">
            Dark Mode Enabled
          </p>
        </div>

        <div className="bg-zinc-900 rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-2">
            Notifications
          </h2>

          <p className="text-zinc-400">
            Email Notifications Enabled
          </p>
        </div>

        <div className="bg-zinc-900 rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-2">
            Account
          </h2>

          <button className="bg-red-600 px-5 py-3 rounded-xl">
            Logout
          </button>
        </div>

      </div>
    </main>
  );
}