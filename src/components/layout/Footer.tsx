import { NAME } from "@/data/content";

export function Footer() {
  return (
    <footer className="mt-20 border-t border-line">
      <div className="mx-auto max-w-5xl px-5 py-8 sm:px-8">
        <p className="kicker" aria-hidden>
          ▸▸▸▸▸▸▸▸▸▸▸▸
        </p>
        <p className="mt-3 text-xs text-muted">
          © 2026 {NAME} · built with Next.js
        </p>
      </div>
    </footer>
  );
}
