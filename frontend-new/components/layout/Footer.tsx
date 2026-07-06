import Container from "../ui/Container";

export default function Footer() {
  return (
    <footer className="border-t border-zinc-800 py-8">
      <Container>
        <div className="flex flex-col md:flex-row justify-between items-center text-zinc-400 text-sm">
          <p>© 2026 CineMind AI. All rights reserved.</p>

          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
            <a href="#">GitHub</a>
          </div>
        </div>
      </Container>
    </footer>
  );
}