# laroccod.github.io

Personal portfolio for Daniel La Rocco: Physics Ph.D. (UC Irvine, 2026) and
scientific software developer. A Next.js rewrite of the earlier Flet site,
built as a dark terminal dashboard: monospace type, glowing stat numerals,
and a physics-glyph "matrix rain".

Live at [laroccod.github.io](https://laroccod.github.io), built and published
by GitHub Actions on every push to `main`.

## Stack

- Next.js 16 (App Router, Turbopack) + React 19 + TypeScript, with the
  experimental View Transitions flag for cross-page fades
- Tailwind CSS v4 (CSS-first tokens in `src/app/globals.css`)
- next-themes for the three-theme cycle: dark → light (UCI blue) → matrix
  (phosphor green, the default)
- Space Mono via next/font (Roboto Mono, greek subset, for the rain canvas;
  `@fontsource/space-mono` as a dev dependency feeds the OG image renderer)
- No other runtime dependencies

## Commands

```bash
npm run dev     # dev server at http://localhost:3000
npm run build   # production build; every route must stay fully static (○)
npm run lint    # eslint
```

## Structure

| Path | Purpose |
|---|---|
| `src/data/content.ts` | All site text: bio, thesis, publications, talks, teaching, contact. Single source of truth. |
| `src/data/projects.ts` | Project registry; link buttons render only for non-empty URLs. |
| `src/data/stats.ts` | Big-number stats, derived from the data arrays so they never drift. |
| `src/data/github.ts` | Build-time GitHub tracker for the "commits" hero stat, with a baked-in fallback count. |
| `src/app/globals.css` | Design tokens for all three themes, terminal card styles, animations. |
| `src/app/*/page.tsx` | The six routes: `/`, `/cv`, `/papers` (nav label "Research"), `/teaching`, `/projects`, `/contact` (`/presentations` meta-refreshes to `/papers`). `not-found.tsx` is the SIGNAL LOST 404. |
| `src/app/og/*.png/route.tsx` | Per-route OG cards, rendered at build time via `src/lib/og.tsx`. Route handlers rather than Next's `opengraph-image` convention, so the emitted file keeps a `.png` extension (see Deployment). |
| `src/lib/` | `site.ts` (canonical origin), `og.tsx` (card renderer), `og-cards.ts` (card copy, alt text, and the `ogMeta()` helper pages use), `use-hydrated.ts` (SSR-safe "am I on the client yet" hook). |
| `src/components/` | `layout/` (navbar, footer, theme toggle, command palette), `ui/` (cards, stats, lightbox, disclosures, typewriter, scroll reveal, status chips), `hero/` (wordmark, matrix rain, thesis diagram), `cards/` (publication, talk, project, contact). |
| `public/` | Headshot, paper figures, talk PDFs and slide previews, project screenshots (mirrors of each project repo's README assets). |

## Content rules

- No em-dashes in user-facing text (use colons, commas, parentheses; en-dashes
  are fine in ranges). Paper abstracts are transcribed verbatim.
- The private `content/` directory convention from the old repo carries over:
  it is gitignored and must never be committed. No phone number anywhere.
- Content changes go in `src/data/*.ts`, never inline in components.

## Design system

Use the CSS-variable Tailwind classes (`bg-bg`, `text-ink`,
`text-accent`, `border-line`, ...), never hardcoded colors; reuse
`TerminalCard`, `SectionHeader`, `StatRow`, `LinkButton`, `Chip`,
`FigureStrip`, `TypedText`, `StatusChip`, and the `.figure-frame` wrapper for
images; paper figures get a white mat, app screenshots do not
(`matted={false}`); every decorative animation respects
`prefers-reduced-motion`; new tokens must be defined for all three theme
blocks.

Interactive extras: ⌘K / Ctrl+K / `/` opens a terminal-style command palette;
the hero rain reacts to the pointer; cards flicker in on scroll; the thesis
card draws an SVG schematic of the signal topology.

## Deployment

`.github/workflows/deploy.yml` builds the site and publishes it to GitHub
Pages on every push to `main` (plus a weekly cron, so the build-time commit
stat stays current). Pages is served from the Actions artifact, not a branch.

`next.config.ts` sets `output: "export"`, so `npm run build` writes a fully
static site to `out/`. That mode has four consequences worth remembering:

- `images.unoptimized` is required, since the default `next/image` loader
  needs a server.
- Every generated route (the OG cards, `sitemap.ts`, `robots.ts`) must declare
  `export const dynamic = "force-static"` or the build fails.
- `trailingSlash: true` emits `cv/index.html` rather than `cv.html`, which is
  what a plain static host expects.
- There is no server to issue a redirect, so `redirect()` bakes an error shell
  into the HTML. `/presentations` uses a meta refresh instead.

OG cards are route handlers under `src/app/og/`, not `opengraph-image.tsx`
files. The file convention emits an extensionless file, and GitHub Pages types
responses by extension, so those cards went out as `application/octet-stream`
and crawlers could refuse them. A route segment ending in `.png` keeps the
cards generated at build time while landing on disk with an extension a static
host understands. Pages opt in with `ogMeta(slug)` from `src/lib/og-cards.ts`.

The build resolves the "commits" hero stat from the GitHub API and logs the
outcome as `[github] ...`, so an Actions run always states whether the number
is real or the baked-in fallback. See `src/data/github.ts` for why the
`/stats/contributors` endpoint cannot be used and why the queries are
sequential.

The canonical origin lives in `src/lib/site.ts`; moving to a custom domain is
a one-line change there (plus a `CNAME` file and DNS records).
