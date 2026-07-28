"use client";

import { useEffect, useRef } from "react";

const GLYPHS = "ψνμπλφητρσξδεθΣΔΩΛΦΨ∂∫≈∞√±0123456789";
const FRAME_MS = 1000 / 30;
const CELL = 18;

function hexToRgb(hex: string): [number, number, number] {
  const h = hex.replace("#", "").trim();
  const full =
    h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  const n = parseInt(full, 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

/** Decorative physics-glyph rain band, ported from the old site's Flet
 * component. Pure canvas: pauses offscreen and on hidden tabs, re-reads
 * theme colors when html.class changes, renders a single static frame
 * under prefers-reduced-motion. */
export function MatrixRain({ className }: { className?: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    let accent = "#faeb92";
    let bgRgb: [number, number, number] = [5, 5, 5];
    const readColors = () => {
      const style = getComputedStyle(document.documentElement);
      accent = style.getPropertyValue("--accent").trim() || accent;
      const bg = style.getPropertyValue("--bg").trim();
      if (bg.startsWith("#")) bgRgb = hexToRgb(bg);
    };
    readColors();

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    let width = 0;
    let height = 0;
    let drops: { y: number; speed: number }[] = [];

    // Pointer perturbation: glyphs near the cursor glow and deflect.
    // The canvas is pointer-events-none, so listen on its parent.
    const pointer = { x: -1e4, y: -1e4 };
    const parent = canvas.parentElement;
    const onPointerMove = (e: PointerEvent) => {
      const rect = canvas.getBoundingClientRect();
      pointer.x = e.clientX - rect.left;
      pointer.y = e.clientY - rect.top;
    };
    const onPointerLeave = () => {
      pointer.x = -1e4;
      pointer.y = -1e4;
    };
    const POINTER_R2 = 90 * 90;

    const font = getComputedStyle(canvas).getPropertyValue("--font-rain");

    const resize = () => {
      width = canvas.clientWidth;
      height = canvas.clientHeight;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const columns = Math.ceil(width / CELL);
      drops = Array.from({ length: columns }, (_, i) => ({
        y: -((i * 7919) % Math.max(height, 1)),
        speed: 0.6 + ((i * 104729) % 100) / 100,
      }));
      ctx.fillStyle = `rgb(${bgRgb.join(",")})`;
      ctx.fillRect(0, 0, width, height);
      // Pre-simulate so the band is never blank on first paint (or in
      // hidden/background tabs where the rAF loop stays paused).
      for (let k = 0; k < 90; k++) drawFrame(false);
    };

    const drawFrame = (full: boolean) => {
      ctx.fillStyle = `rgba(${bgRgb.join(",")},${full ? 1 : 0.09})`;
      ctx.fillRect(0, 0, width, height);
      ctx.font = `13px ${font || "monospace"}`;
      for (let i = 0; i < drops.length; i++) {
        const drop = drops[i];
        const idx = i * 31 + Math.floor(Math.abs(drop.y) / CELL) * 7;
        const glyph = GLYPHS[idx % GLYPHS.length];
        if (drop.y >= 0) {
          const x = i * CELL;
          const dx = x - pointer.x;
          const dy = drop.y - pointer.y;
          const d2 = dx * dx + dy * dy;
          ctx.fillStyle = accent;
          if (d2 < POINTER_R2) {
            // Near the cursor: full brightness, pushed gently outward.
            const push = (1 - d2 / POINTER_R2) * 10;
            ctx.globalAlpha = 1;
            ctx.fillText(glyph, x + (dx >= 0 ? push : -push), drop.y);
          } else {
            ctx.globalAlpha = 0.85;
            ctx.fillText(glyph, x, drop.y);
          }
          ctx.globalAlpha = 1;
        }
        drop.y += drop.speed * CELL * 0.36;
        if (drop.y > height + CELL) {
          drop.y = -CELL * (1 + ((i * 13) % 20));
        }
      }
    };
    resize();

    if (reduced) {
      // Static frame: scatter glyphs once, no animation.
      ctx.fillStyle = `rgb(${bgRgb.join(",")})`;
      ctx.fillRect(0, 0, width, height);
      ctx.font = `13px ${font || "monospace"}`;
      ctx.fillStyle = accent;
      ctx.globalAlpha = 0.35;
      for (let i = 0; i < drops.length; i++) {
        for (let j = 0; j < 3; j++) {
          const y = ((i * 7919 + j * 104729) % Math.max(height, 1));
          ctx.fillText(GLYPHS[(i + j * 11) % GLYPHS.length], i * CELL, y);
        }
      }
      ctx.globalAlpha = 1;
      return;
    }

    parent?.addEventListener("pointermove", onPointerMove);
    parent?.addEventListener("pointerleave", onPointerLeave);

    let raf = 0;
    let last = 0;
    let visible = true;
    const loop = (now: number) => {
      raf = requestAnimationFrame(loop);
      if (!visible || document.visibilityState === "hidden") return;
      if (now - last < FRAME_MS) return;
      last = now;
      drawFrame(false);
    };
    raf = requestAnimationFrame(loop);

    const io = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
    });
    io.observe(canvas);

    const ro = new ResizeObserver(resize);
    ro.observe(canvas);

    // Re-read palette when the theme class flips on <html>.
    const mo = new MutationObserver(() => {
      readColors();
      ctx.fillStyle = `rgb(${bgRgb.join(",")})`;
      ctx.fillRect(0, 0, width, height);
    });
    mo.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });

    return () => {
      cancelAnimationFrame(raf);
      io.disconnect();
      ro.disconnect();
      mo.disconnect();
      parent?.removeEventListener("pointermove", onPointerMove);
      parent?.removeEventListener("pointerleave", onPointerLeave);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden
      className={`pointer-events-none ${className ?? ""}`}
      style={{
        maskImage:
          "linear-gradient(to bottom, transparent, black 15%, black 80%, transparent)",
        WebkitMaskImage:
          "linear-gradient(to bottom, transparent, black 15%, black 80%, transparent)",
      }}
    />
  );
}
