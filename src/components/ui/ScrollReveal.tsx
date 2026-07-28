"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";

/** Site-wide scroll reveal: terminal cards below the fold flicker in as
 * they enter the viewport (CRT-redraw effect, see card-reveal in
 * globals.css). Mounted once in the root layout; re-scans on route
 * change. Cards stay fully visible under prefers-reduced-motion and
 * before hydration, so nothing is ever hidden without JS. */
export function ScrollReveal() {
  const pathname = usePathname();

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const cards = Array.from(
      document.querySelectorAll<HTMLElement>(".terminal-card"),
    ).filter(
      (el) =>
        !el.classList.contains("reveal-in") &&
        // Only defer cards that are still comfortably below the fold;
        // anything already (nearly) visible stays put.
        el.getBoundingClientRect().top > window.innerHeight * 0.95,
    );
    if (cards.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          entry.target.classList.remove("reveal-pending");
          entry.target.classList.add("reveal-in");
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.08 },
    );
    for (const el of cards) {
      el.classList.add("reveal-pending");
      observer.observe(el);
    }
    return () => {
      observer.disconnect();
      // Never leave cards hidden across navigations
      for (const el of cards) el.classList.remove("reveal-pending");
    };
  }, [pathname]);

  return null;
}
