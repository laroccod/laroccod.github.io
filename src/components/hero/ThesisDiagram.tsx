"use client";

import { useEffect, useRef, useState } from "react";

/** Stroke-draw delay helper: each group traces in sequence. */
const delay = (ms: number) => ({ "--draw-delay": `${ms}ms` }) as React.CSSProperties;

/** Line-art schematic of the thesis signal topology: an HNL produced at
 * the ATLAS interaction point travels ~650 m and decays to μπ inside
 * FASER2. Strokes trace themselves in when scrolled into view
 * (diagram-draw / drawn classes in globals.css); labels fade in after.
 * Static under prefers-reduced-motion via the same CSS. */
export function ThesisDiagram() {
  const ref = useRef<SVGSVGElement>(null);
  const [drawn, setDrawn] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        setDrawn(true);
      },
      { threshold: 0.35 },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <svg
      ref={ref}
      viewBox="0 0 720 170"
      role="img"
      aria-label="Schematic: a heavy neutral lepton produced at the ATLAS interaction point travels 650 meters and decays to a muon and a pion inside FASER2"
      className={`diagram-draw mt-6 w-full max-w-[560px] ${drawn ? "drawn" : ""}`}
      strokeWidth="1.5"
      strokeLinecap="square"
      fill="none"
    >
      {/* ATLAS: interaction-point rings */}
      <g className="text-muted" stroke="currentColor" style={delay(0)}>
        <circle cx="72" cy="78" r="36" pathLength="1" />
        <circle cx="72" cy="78" r="22" pathLength="1" />
      </g>
      <circle
        cx="72"
        cy="78"
        r="4"
        pathLength="1"
        className="text-accent"
        stroke="currentColor"
        style={delay(150)}
      />
      {/* beam axis through the IP */}
      <line
        x1="10"
        y1="78"
        x2="36"
        y2="78"
        pathLength="1"
        className="text-muted"
        stroke="currentColor"
        style={delay(100)}
      />

      {/* HNL line of flight, with distance bracket below */}
      <line
        x1="108"
        y1="78"
        x2="468"
        y2="78"
        pathLength="1"
        className="text-accent"
        stroke="currentColor"
        style={delay(280)}
      />
      <path
        d="M 460 74 L 468 78 L 460 82"
        pathLength="1"
        className="text-accent"
        stroke="currentColor"
        style={delay(500)}
      />
      <path
        d="M 130 108 L 130 116 L 446 116 L 446 108"
        pathLength="1"
        className="text-muted"
        stroke="currentColor"
        style={delay(500)}
      />

      {/* FASER2 decay volume */}
      <rect
        x="480"
        y="46"
        width="170"
        height="64"
        pathLength="1"
        className="text-muted"
        stroke="currentColor"
        style={delay(650)}
      />
      {/* decay vertex and μ / π tracks */}
      <line
        x1="480"
        y1="78"
        x2="530"
        y2="78"
        pathLength="1"
        className="text-accent"
        stroke="currentColor"
        style={delay(800)}
      />
      <line
        x1="530"
        y1="78"
        x2="644"
        y2="56"
        pathLength="1"
        className="text-secondary"
        stroke="currentColor"
        style={delay(950)}
      />
      <line
        x1="530"
        y1="78"
        x2="644"
        y2="100"
        pathLength="1"
        className="text-secondary"
        stroke="currentColor"
        style={delay(950)}
      />
      <circle
        cx="530"
        cy="78"
        r="3.5"
        pathLength="1"
        className="text-accent"
        stroke="currentColor"
        style={delay(900)}
      />

      {/* labels */}
      <g
        className="font-mono text-muted"
        fill="currentColor"
        fontSize="12"
        style={delay(1150)}
      >
        <text x="72" y="140" textAnchor="middle">
          ATLAS
        </text>
        <text x="288" y="134" textAnchor="middle">
          ~650 m
        </text>
        <text x="565" y="140" textAnchor="middle">
          FASER2
        </text>
      </g>
      <g className="font-mono" fill="currentColor" fontSize="13" style={delay(1300)}>
        <text x="284" y="66" textAnchor="middle" className="text-accent">
          N
        </text>
        <text x="656" y="58" className="text-secondary">
          μ
        </text>
        <text x="656" y="106" className="text-secondary">
          π
        </text>
      </g>
    </svg>
  );
}
