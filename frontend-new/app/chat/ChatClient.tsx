"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { createChat, sendChatMessage } from "@/lib/api";

type Message = {
  role: string;
  content: string;
};

export default function ChatClient() {
  const [chatId, setChatId] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi 👋 I'm CineMind AI. Ask me anything about movies.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const searchParams = useSearchParams();
  const movie = searchParams.get("movie");

  useEffect(() => {
    async function init() {
      try {
        const chat = await createChat();
        setChatId(chat.id);
      } catch (err) {
        console.error(err);
      }
    }

    init();

    if (movie) {
      setMessages([
        {
          role: "assistant",
          content: `🎬 Let's talk about "${movie}". Ask me anything about this movie!`,
        },
      ]);
    }
  }, [movie]);

  async function sendMessage() {
    if (!input.trim()) return;
    if (!chatId) return;

    const text = input;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: text,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await sendChatMessage(chatId, text);

      console.log("BACKEND RESPONSE:", response);

      setMessages((prev) => [
        ...prev,
        ...response,
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong 😢",
        },
      ]);
    }

    setLoading(false);
  }

  return (
    <main className="min-h-screen bg-black text-white flex flex-col">
      <div className="flex-1 max-w-4xl mx-auto w-full p-8">
        <h1 className="text-5xl font-bold mb-8">
          🤖 CineMind AI
        </h1>

        <div className="space-y-6">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`rounded-2xl p-4 max-w-xl ${
                msg.role === "user"
                  ? "ml-auto bg-red-600"
                  : "bg-zinc-800"
              }`}
            >
              {msg.content}
            </div>
          ))}

          {loading && (
            <div className="bg-zinc-800 rounded-2xl p-4 w-fit">
              Thinking...
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-zinc-800 p-6">
        <div className="max-w-4xl mx-auto flex gap-4">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            placeholder="Ask CineMind..."
            className="flex-1 rounded-xl bg-zinc-900 px-5 py-4 outline-none"
          />

          <button
            onClick={sendMessage}
            className="bg-red-600 px-8 rounded-xl"
          >
            Send
          </button>
        </div>
      </div>
    </main>
  );
}