import { Suspense } from "react";
import ChatClient from "./ChatClient";

export default function Page() {
  return (
    <Suspense fallback={<div className="p-8 text-white">Loading...</div>}>
      <ChatClient />
    </Suspense>
  );
}