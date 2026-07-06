import Navbar from "@/components/layout/Navbar";
import Hero from "@/components/home/Hero";
import FeaturedBanner from "@/components/home/FeaturedBanner";
import TrendingMovies from "@/components/home/TrendingMovies";
import Features from "@/components/home/Features";
import ChatPreview from "@/components/home/ChatPreview";
import CTA from "@/components/home/CTA";
import Footer from "@/components/layout/Footer";
import TopRatedMovies from "@/components/home/TopRatedMovies";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white">

      <Navbar />

      <Hero />

      <FeaturedBanner />

      <TrendingMovies />

      <TopRatedMovies />

      <Features />

      <ChatPreview />

      <CTA />

      <Footer />

    </main>
  );
}