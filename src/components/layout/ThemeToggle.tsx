"use client";

import { useTheme } from "next-themes";
import { useHydrated } from "@/lib/use-hydrated";

const CYCLE = ["dark", "light", "matrix"] as const;

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const mounted = useHydrated();

  const current = CYCLE.indexOf(resolvedTheme as (typeof CYCLE)[number]);
  const next = CYCLE[(current + 1) % CYCLE.length] ?? "light";

  return (
    <button
      type="button"
      aria-label="Cycle color theme"
      onClick={() => setTheme(next)}
      className="w-[10ch] whitespace-nowrap text-left text-[13px] tracking-wide text-muted transition-colors hover:text-accent"
    >
      {mounted && current !== -1 ? `[ ${CYCLE[current]} ]` : "[ ····· ]"}
    </button>
  );
}
