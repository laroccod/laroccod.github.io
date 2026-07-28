"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { useHydrated } from "@/lib/use-hydrated";
import { ThemeToggle } from "./ThemeToggle";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/cv", label: "CV" },
  { href: "/papers", label: "Research" },
  { href: "/teaching", label: "Teaching" },
  { href: "/projects", label: "Projects" },
  { href: "/contact", label: "Contact" },
];

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  // The palette shortcut is ⌘K on Apple hardware and Ctrl+K everywhere else
  // (CommandPalette accepts either). The server cannot know which, so the
  // label waits for hydration, like ThemeToggle's.
  const hydrated = useHydrated();
  const shortcut = hydrated
    ? /Mac|iPhone|iPad|iPod/i.test(navigator.userAgent)
      ? "⌘k"
      : "ctrl k"
    : null;

  return (
    <header className="sticky top-0 z-40 border-b border-line bg-bg/90 backdrop-blur-sm">
      <nav className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-5 py-3 sm:px-8">
        <Link
          href="/"
          className="brand flex items-center text-sm font-bold tracking-widest text-ink"
          onClick={() => setOpen(false)}
        >
          <span className="brand-prompt mr-2 text-accent" aria-hidden>
            ▸
          </span>
          DLR
          <span className="brand-cursor" aria-hidden />
        </Link>

        <div className="hidden items-center gap-1 min-[850px]:flex">
          {LINKS.map((link) => {
            const active =
              link.href === "/"
                ? pathname === "/"
                : pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`px-3 py-1.5 text-[13px] tracking-wide transition-colors ${
                  active
                    ? "text-accent border-b border-accent"
                    : "text-muted hover:text-ink"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
          <span className="ml-2">
            <ThemeToggle />
          </span>
          <button
            type="button"
            aria-label="Open command palette"
            onClick={() => window.dispatchEvent(new Event("open-command-palette"))}
            className="w-[11ch] whitespace-nowrap px-1 text-left text-[13px] tracking-wide text-muted transition-colors hover:text-accent"
          >
            {shortcut ? `[ ${shortcut} ]` : "[ ···· ]"}
          </button>
        </div>

        <div className="flex items-center gap-3 min-[850px]:hidden">
          <ThemeToggle />
          <button
            type="button"
            aria-expanded={open}
            aria-label={open ? "Close menu" : "Open menu"}
            onClick={() => setOpen((v) => !v)}
            className="px-2 py-1 text-[13px] text-muted hover:text-ink"
          >
            {open ? "[ close ]" : "[ menu ]"}
          </button>
        </div>
      </nav>

      {open && (
        <div className="border-t border-line bg-bg min-[850px]:hidden">
          {LINKS.map((link) => {
            const active =
              link.href === "/"
                ? pathname === "/"
                : pathname.startsWith(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className={`block px-6 py-3 text-[13px] tracking-wide ${
                  active ? "text-accent" : "text-muted"
                }`}
              >
                {active ? "▸ " : "  "}
                {link.label}
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
