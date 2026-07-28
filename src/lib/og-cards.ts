import type { Metadata } from "next";
import { NAME } from "@/data/content";

export const OG_SIZE = { width: 1200, height: 630 };

interface OgCard {
  kicker: string;
  title: string;
  subtitle: string;
  /** Alt text for the card, used in the page metadata. */
  alt: string;
}

/** One card per route with an Open Graph preview. The keys double as the
 * filenames served under /og/. */
export const OG_CARDS = {
  home: {
    kicker: ">> Orange County, CA // online",
    title: NAME,
    subtitle: "Physics Ph.D. / Scientific Software Developer",
    alt: `${NAME} - Physics Ph.D. and scientific software developer`,
  },
  cv: {
    kicker: ">> Section 01 // curriculum vitae",
    title: "CV",
    subtitle: NAME,
    alt: `Curriculum vitae of ${NAME}`,
  },
  research: {
    kicker: ">> Section 02 // papers & talks",
    title: "Research",
    subtitle: NAME,
    alt: `Research by ${NAME}: papers and talks`,
  },
  teaching: {
    kicker: ">> Section 03 // instruction",
    title: "Teaching",
    subtitle: NAME,
    alt: `Teaching experience of ${NAME}`,
  },
  projects: {
    kicker: ">> Section 04 // software",
    title: "Projects",
    subtitle: NAME,
    alt: `Open-source projects by ${NAME}`,
  },
  contact: {
    kicker: ">> Section 05 // transmission",
    title: "Contact",
    subtitle: NAME,
    alt: `Contact ${NAME}`,
  },
} satisfies Record<string, OgCard>;

export type OgSlug = keyof typeof OG_CARDS;

/** Points a page's metadata at its card under /og/<slug>.png.
 *
 * The cards are route handlers rather than Next's `opengraph-image` file
 * convention because that convention emits an extensionless file. GitHub
 * Pages types responses by file extension, so it labels such a file
 * `application/octet-stream` and crawlers may refuse to render the preview.
 * A route segment ending in `.png` keeps the generation dynamic and still
 * lands on disk with an extension a static host understands. */
export function ogMeta(slug: OgSlug): Metadata {
  const images = [{ url: `/og/${slug}.png`, ...OG_SIZE, alt: OG_CARDS[slug].alt }];
  return {
    openGraph: { images },
    twitter: { card: "summary_large_image", images },
  };
}
