"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import type { Stat } from "@/data/types";

/** Count from 0 to target over ~1s once the element scrolls into view.
 * Skips straight to the target under prefers-reduced-motion. */
function useCountUp(target: number) {
  const ref = useRef<HTMLSpanElement>(null);
  const [value, setValue] = useState(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setValue(target);
      return;
    }
    let raf = 0;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        const start = performance.now();
        const duration = 1400;
        const tick = (now: number) => {
          const t = Math.min(Math.max((now - start) / duration, 0), 1);
          const eased = 1 - Math.pow(1 - t, 3);
          setValue(Math.round(eased * target));
          if (t < 1) raf = requestAnimationFrame(tick);
        };
        raf = requestAnimationFrame(tick);
      },
      { threshold: 0.2 },
    );
    observer.observe(el);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(raf);
    };
  }, [target]);

  return { ref, value };
}

function StatBody({ stat }: { stat: Stat }) {
  const { ref, value } = useCountUp(stat.value);
  const numeral = stat.pad
    ? String(value).padStart(stat.pad, "0")
    : String(value);
  return (
    <>
      <span ref={ref} className="stat-numeral text-5xl font-bold sm:text-6xl">
        {numeral}
        {stat.suffix && (
          <span className="text-secondary text-4xl sm:text-5xl">
            {stat.suffix}
          </span>
        )}
      </span>
      <span className="kicker mt-3 block">{stat.label}</span>
    </>
  );
}

export function StatCard({ stat }: { stat: Stat }) {
  const inner = <StatBody stat={stat} />;
  const className =
    "terminal-card block px-5 py-6 text-left transition-transform";
  if (stat.href) {
    if (/^https?:/.test(stat.href)) {
      return (
        <a
          href={stat.href}
          target="_blank"
          rel="noopener noreferrer"
          className={className}
        >
          {inner}
        </a>
      );
    }
    return (
      <Link href={stat.href} className={className}>
        {inner}
      </Link>
    );
  }
  return <div className={className}>{inner}</div>;
}

export function StatRow({ stats }: { stats: Stat[] }) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {stats.map((stat) => (
        <StatCard key={stat.label} stat={stat} />
      ))}
    </div>
  );
}
