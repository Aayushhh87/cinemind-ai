import Card from "@/components/ui/Card";

const features = [
  {
    title: "AI Movie Search",
    description: "Search movies using natural language with AI.",
  },
  {
    title: "Smart Recommendations",
    description: "Get personalized movie suggestions instantly.",
  },
  {
    title: "Chat Assistant",
    description: "Talk with CineMind AI about movies and TV shows.",
  },
];

export default function Features() {
  return (
    <section className="bg-zinc-950 px-6 py-20">
      <div className="mx-auto max-w-6xl">
        <h2 className="mb-12 text-center text-4xl font-bold">
          Why CineMind?
        </h2>

        <div className="grid gap-8 md:grid-cols-3">
          {features.map((feature) => (
            <Card key={feature.title}>
              <h3 className="mb-3 text-xl font-semibold">
                {feature.title}
              </h3>

              <p className="text-zinc-400">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}