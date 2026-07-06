export default function ProfilePage() {
  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-5xl font-bold mb-10">
        👤 My Profile
      </h1>

      <div className="bg-zinc-900 rounded-2xl p-8 max-w-xl space-y-4">
        <p>
          <span className="font-bold">Username:</span> Demo User
        </p>

        <p>
          <span className="font-bold">Email:</span> demo@cinemind.ai
        </p>

        <p>
          <span className="font-bold">Favorite Movies:</span> 0
        </p>

        <p>
          <span className="font-bold">Chats:</span> 0
        </p>
      </div>
    </main>
  );
}