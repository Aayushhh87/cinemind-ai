import Button from "@/components/ui/Button";
import Container from "@/components/ui/Container";

export default function Home() {
  return (
    <main className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      <Container>
        <section className="flex min-h-screen flex-col items-center justify-center text-center">
          <h1 className="text-5xl font-bold tracking-tight md:text-7xl">
            🎬 CineMind AI
          </h1>

          <p className="mt-6 max-w-2xl text-lg text-[var(--secondary)]">
            Search movies, explore stories, and chat with AI to discover
            everything about your favorite films.
          </p>

          <div className="mt-8">
            <Button>Get Started</Button>
          </div>
        </section>
      </Container>
    </main>
  );
}