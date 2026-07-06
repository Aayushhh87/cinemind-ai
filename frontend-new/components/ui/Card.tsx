import { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export default function Card({
  children,
  className = "",
}: CardProps) {
  return (
    <div
      className={`
        rounded-[var(--radius)]
        border
        border-[var(--border)]
        bg-[var(--surface)]
        p-6
        shadow-lg
        transition-all
        duration-300
        hover:-translate-y-1
        hover:border-red-600
        hover:shadow-red-600/10
        ${className}
      `}
    >
      {children}
    </div>
  );
}