const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL!;

console.log("BACKEND =", BACKEND);
// =====================
// Semantic Search
// =====================
export async function semanticSearch(query: string) {
  const res = await fetch(
    `${BACKEND}/api/v1/search/semantic`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        limit: 10,
      }),
    }
  );

  if (!res.ok) {
    throw new Error("Search failed");
  }

  return res.json();
}

// =====================
// Chat APIs
// =====================

export async function createChat() {
  const res = await fetch(`${BACKEND}/api/v1/chats`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: "New Chat",
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to create chat");
  }

  return await res.json();
}


export async function sendChatMessage(
  chatId: string,
  content: string
) {
  const res = await fetch(
    `${BACKEND}/api/v1/chats/${chatId}/messages`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content,
      }),
    }
  );

  if (!res.ok) {
    throw new Error("Failed to send message");
  }

  return res.json();
}

export async function getChat(chatId: string) {
  const res = await fetch(
    `${BACKEND}/api/v1/chats/${chatId}`
  );

  if (!res.ok) {
    throw new Error("Failed to load chat");
  }

  return res.json();
}
