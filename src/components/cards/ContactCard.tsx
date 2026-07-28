import type { Link as ContactLink } from "@/data/types";

const GLYPHS: Record<string, string> = {
  EMAIL: "✉",
  CODE: "⌥",
  WORK: "☍",
  BADGE: "❖",
};

export function ContactCard({ link }: { link: ContactLink }) {
  const display = link.url.replace(/^(mailto:|https?:\/\/)/, "").replace(/\/$/, "");
  return (
    <a
      href={link.url}
      {...(link.url.startsWith("http")
        ? { target: "_blank", rel: "noopener noreferrer" }
        : {})}
      className="terminal-card flex items-center gap-4 p-5 transition-colors"
    >
      <span className="text-2xl text-accent" aria-hidden>
        {GLYPHS[link.icon ?? ""] ?? "▸"}
      </span>
      <span className="min-w-0">
        <span className="block text-[15px] font-bold">{link.label}</span>
        <span className="block truncate text-[13px] text-muted">{display}</span>
      </span>
      <span className="ml-auto text-muted" aria-hidden>
        ↗
      </span>
    </a>
  );
}
