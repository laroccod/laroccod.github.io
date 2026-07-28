import { ImageResponse } from "next/og";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

/** Shared Open Graph card in the site's BFCM terminal style: dark panel,
 * hairline border, gold corner ticks, Space Mono throughout. Colors are
 * the dark-theme tokens from globals.css (OG images can't read CSS vars,
 * and the dark theme is the site default). ASCII-only text: satori only
 * has the glyphs in the two font files loaded below. */

export const OG_SIZE = { width: 1200, height: 630 };

const BG = "#050505";
const PANEL = "#0c0a10";
const LINE = "#241a33";
const INK = "#f6eefc";
const MUTED = "#a794be";
const ACCENT = "#faeb92";

const FONT_DIR = join(
  process.cwd(),
  "node_modules/@fontsource/space-mono/files",
);

interface OgCardProps {
  kicker: string;
  title: string;
  subtitle: string;
}

export async function ogCard({ kicker, title, subtitle }: OgCardProps) {
  const [regular, bold] = await Promise.all([
    readFile(join(FONT_DIR, "space-mono-latin-400-normal.woff")),
    readFile(join(FONT_DIR, "space-mono-latin-700-normal.woff")),
  ]);

  const tick = {
    position: "absolute" as const,
    width: 18,
    height: 18,
    borderColor: ACCENT,
    borderStyle: "solid",
  };

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          backgroundColor: BG,
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(246,238,252,0.07) 1px, transparent 0)`,
          backgroundSize: "32px 32px",
          padding: 56,
          fontFamily: "Space Mono",
        }}
      >
        <div
          style={{
            position: "relative",
            display: "flex",
            flexDirection: "column",
            justifyContent: "space-between",
            width: "100%",
            height: "100%",
            border: `2px solid ${LINE}`,
            backgroundColor: PANEL,
            padding: 64,
          }}
        >
          <div style={{ ...tick, top: -2, left: -2, borderWidth: "3px 0 0 3px" }} />
          <div style={{ ...tick, bottom: -2, right: -2, borderWidth: "0 3px 3px 0" }} />

          <div
            style={{
              display: "flex",
              fontSize: 28,
              letterSpacing: "0.18em",
              color: ACCENT,
            }}
          >
            {kicker.toUpperCase()}
          </div>

          <div
            style={{
              display: "flex",
              fontSize: title.length > 40 ? 56 : 72,
              fontWeight: 700,
              lineHeight: 1.15,
              color: INK,
            }}
          >
            {title}
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontSize: 26,
              color: MUTED,
            }}
          >
            <span>{subtitle}</span>
            <span style={{ color: ACCENT }}>[ dlr ]</span>
          </div>
        </div>
      </div>
    ),
    {
      ...OG_SIZE,
      fonts: [
        { name: "Space Mono", data: regular, style: "normal", weight: 400 },
        { name: "Space Mono", data: bold, style: "normal", weight: 700 },
      ],
    },
  );
}
