export default function DashboardPage() {
  const stats = [
    { title: "Favorites", value: 12 },
    { title: "Chats", value: 8 },
    { title: "Recommendations", value: 35 },
    { title: "Movies Viewed", value: 102 },
  ];

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-5xl font-bold mb-10">
        📊 Dashboard
      </h1>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((item) => (
          <div
            key={item.title}
            className="bg-zinc-900 rounded-2xl p-6"
          >
            <h2 className="text-zinc-400">
              {item.title}
            </h2>

            <p className="text-4xl font-bold mt-3">
              {item.value}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}