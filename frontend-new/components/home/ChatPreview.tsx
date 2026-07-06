import Card from "@/components/ui/Card";

export default function ChatPreview() {
  return (
    <section className="px-6 py-24">
      <div className="mx-auto max-w-4xl">
        <h2 className="mb-10 text-center text-4xl font-bold">
          Talk with CineMind AI
        </h2>

        <Card className="space-y-6">
          <div className="flex justify-end">
            <div className="max-w-md rounded-2xl bg-red-600 px-5 py-3 text-white">
              Recommend me movies like Interstellar
            </div>
          </div>

          <div className="flex justify-start">
            <div className="max-w-md rounded-2xl bg-zinc-800 px-5 py-3">
              ⭐ Based on Interstellar, you might enjoy:
              <br /><br />
              • Arrival
              <br />
              • Blade Runner 2049
              <br />
              • Contact
              <br />
              • The Martian
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
}