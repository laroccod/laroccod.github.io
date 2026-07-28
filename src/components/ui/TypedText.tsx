"use client";

import { useEffect, useRef, useState } from "react";

interface TypedTextProps {
  text: string;
  /** ms per character */
  speed?: number;
  /** ms before typing starts */
  startDelay?: number;
  /** keep the block cursor blinking after typing finishes */
  keepCursor?: boolean;
  className?: string;
}

/** Terminal typewriter: types `text` with a blinking block cursor once the
 * element scrolls into view. A visually-hidden copy of the full text
 * reserves the final layout (no shift) and keeps the copy available to
 * screen readers and crawlers at all times. Renders the finished text
 * immediately under prefers-reduced-motion. */
export function TypedText({
  text,
  speed = 14,
  startDelay = 250,
  keepCursor = false,
  className,
}: TypedTextProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const [count, setCount] = useState(0);
  const done = count >= text.length;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setCount(text.length);
      return;
    }
    let timer = 0;
    let raf = 0;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        timer = window.setTimeout(() => {
          // Time-based, not chained timeouts: the visible count derives
          // from elapsed time, so total duration is exact and scheduling
          // stays outside the state updater (which must remain pure).
          const start = performance.now();
          const step = (now: number) => {
            const n = Math.min(
              Math.floor(Math.max(now - start, 0) / speed),
              text.length,
            );
            setCount(n);
            if (n < text.length) raf = requestAnimationFrame(step);
          };
          raf = requestAnimationFrame(step);
        }, startDelay);
      },
      { threshold: 0.2 },
    );
    observer.observe(el);
    return () => {
      observer.disconnect();
      clearTimeout(timer);
      cancelAnimationFrame(raf);
    };
  }, [text, speed, startDelay]);

  return (
    <span ref={ref} className={`relative block ${className ?? ""}`}>
      <span className={done ? undefined : "invisible"}>{text}</span>
      {!done && (
        <span aria-hidden className="absolute inset-0">
          {text.slice(0, count)}
          <span className="typed-cursor" />
        </span>
      )}
      {done && keepCursor && <span aria-hidden className="typed-cursor" />}
    </span>
  );
}
