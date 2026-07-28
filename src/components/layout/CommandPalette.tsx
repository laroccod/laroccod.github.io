"use client";

import { useRouter } from "next/navigation";
import { useTheme } from "next-themes";
import { useEffect, useRef, useState } from "react";
import { EMAIL, GITHUB } from "@/data/content";

const THEME_CYCLE = ["dark", "light", "matrix"] as const;

interface Command {
  label: string;
  hint: string;
  action: "push" | "external" | "theme";
  target?: string;
}

const COMMANDS: Command[] = [
  { label: "cd ~/home", hint: "Home", action: "push", target: "/" },
  { label: "cd ~/cv", hint: "CV", action: "push", target: "/cv" },
  { label: "cd ~/papers", hint: "Research", action: "push", target: "/papers" },
  { label: "cd ~/teaching", hint: "Teaching", action: "push", target: "/teaching" },
  { label: "cd ~/projects", hint: "Projects", action: "push", target: "/projects" },
  { label: "cd ~/contact", hint: "Contact", action: "push", target: "/contact" },
  { label: "theme --next", hint: "Cycle color theme", action: "theme" },
  { label: "open github", hint: "github.com/laroccod", action: "external", target: GITHUB },
  { label: "mail daniel", hint: EMAIL, action: "external", target: `mailto:${EMAIL}` },
];

/** Terminal-style command palette: ⌘K / Ctrl+K (or `/`) opens a native
 * dialog with fuzzy-ish filtering over navigation and quick actions.
 * The navbar can open it by dispatching "open-command-palette". */
export function CommandPalette() {
  const dialogRef = useRef<HTMLDialogElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const { resolvedTheme, setTheme } = useTheme();
  const [query, setQuery] = useState("");
  const [index, setIndex] = useState(0);

  const matches = COMMANDS.filter((c) =>
    `${c.label} ${c.hint}`.toLowerCase().includes(query.toLowerCase().trim()),
  );
  const active = matches[Math.min(index, Math.max(matches.length - 1, 0))];

  const open = () => {
    const dialog = dialogRef.current;
    if (!dialog || dialog.open) return;
    setQuery("");
    setIndex(0);
    dialog.showModal();
    inputRef.current?.focus();
  };
  const close = () => dialogRef.current?.close();

  const run = (command: Command | undefined) => {
    if (!command) return;
    close();
    if (command.action === "push" && command.target) {
      router.push(command.target);
    } else if (command.action === "external" && command.target) {
      window.open(command.target, "_blank", "noopener,noreferrer");
    } else if (command.action === "theme") {
      const at = THEME_CYCLE.indexOf(
        resolvedTheme as (typeof THEME_CYCLE)[number],
      );
      setTheme(THEME_CYCLE[(at + 1) % THEME_CYCLE.length]);
    }
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const inDialog = dialogRef.current?.open;
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (inDialog) close();
        else open();
        return;
      }
      if (e.key === "/" && !inDialog) {
        const t = e.target as HTMLElement | null;
        const typing =
          t &&
          (t.tagName === "INPUT" ||
            t.tagName === "TEXTAREA" ||
            t.tagName === "SELECT" ||
            t.isContentEditable);
        if (!typing) {
          e.preventDefault();
          open();
        }
      }
    };
    const onOpenEvent = () => open();
    window.addEventListener("keydown", onKey);
    window.addEventListener("open-command-palette", onOpenEvent);
    return () => {
      window.removeEventListener("keydown", onKey);
      window.removeEventListener("open-command-palette", onOpenEvent);
    };
  }, []);

  return (
    <dialog
      ref={dialogRef}
      aria-label="Command palette"
      onClick={(e) => {
        if (e.target === dialogRef.current) close();
      }}
      className="m-auto mt-[18vh] w-[min(560px,92vw)] border border-line-bright bg-panel p-0 text-ink shadow-[0_0_40px_rgba(0,0,0,0.5)] backdrop:bg-black/70 backdrop:backdrop-blur-[2px]"
    >
      <div className="flex items-center gap-2 border-b border-line px-4 py-3">
        <span className="text-accent" aria-hidden>
          &gt;
        </span>
        <input
          ref={inputRef}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIndex(0);
          }}
          onKeyDown={(e) => {
            if (e.key === "ArrowDown") {
              e.preventDefault();
              setIndex((i) => Math.min(i + 1, matches.length - 1));
            } else if (e.key === "ArrowUp") {
              e.preventDefault();
              setIndex((i) => Math.max(i - 1, 0));
            } else if (e.key === "Enter") {
              e.preventDefault();
              run(active);
            }
          }}
          placeholder="type a command or search..."
          spellCheck={false}
          autoComplete="off"
          className="w-full bg-transparent font-mono text-[14px] text-ink placeholder:text-muted focus:outline-none"
        />
        <span className="kicker shrink-0 !text-[10px]" aria-hidden>
          esc
        </span>
      </div>
      <ul className="max-h-[46vh] overflow-y-auto py-2">
        {matches.length === 0 && (
          <li className="px-4 py-2 text-[13px] text-muted">
            command not found: {query}
          </li>
        )}
        {matches.map((command, i) => (
          <li key={command.label}>
            <button
              type="button"
              onClick={() => run(command)}
              onMouseEnter={() => setIndex(i)}
              className={`flex w-full items-baseline justify-between gap-4 px-4 py-2 text-left font-mono text-[13px] transition-colors ${
                command === active
                  ? "bg-surface text-accent"
                  : "text-ink"
              }`}
            >
              <span className="whitespace-nowrap">
                <span aria-hidden>{command === active ? "▸ " : "  "}</span>
                {command.label}
              </span>
              <span className="truncate text-[11px] text-muted">
                {command.hint}
              </span>
            </button>
          </li>
        ))}
      </ul>
    </dialog>
  );
}
