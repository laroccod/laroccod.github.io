/** Shared content types, mirroring the dataclasses in the old site's
 * src/data/content.py so the two sources stay easy to diff. */

export interface Link {
  label: string;
  url: string;
  icon?: string;
}

/** A figure lifted from a paper or the thesis. `src` is a public/ path. */
export interface Figure {
  src: string;
  caption: string;
}

export interface SkillGroup {
  name: string;
  items: string[];
}

export interface Experience {
  role: string;
  org: string;
  dates: string;
  advisor: string;
  bullets: string[];
}

export interface Education {
  school: string;
  degree: string;
  dates: string;
  details: string[];
}

export interface Publication {
  authors: string;
  title: string;
  venue: string;
  year: string;
  url: string;
  /** When set, the papers page shows a "Show abstract" toggle. */
  abstract?: string;
  figures?: Figure[];
}

export interface Presentation {
  date: string;
  kind: string;
  event: string;
  where: string;
  title: string;
  url?: string;
  /** Site-relative PDF path under public/ (e.g. /talks/x.pdf). */
  slides?: string;
  /** Rendered slide images, title slide first. */
  previews?: string[];
}

export interface TeachingRole {
  role: string;
  org: string;
  dates: string;
  bullets: string[];
}

export interface Project {
  slug: string;
  name: string;
  tagline: string;
  description: string;
  tech: string[];
  role?: string;
  githubUrl?: string;
  pypiUrl?: string;
  /** When set, a "Launch live demo" button appears. */
  demoUrl?: string;
  docsUrl?: string;
  screenshots?: string[];
  featured?: boolean;
}

export interface Stat {
  /** Numeric part, counted up on scroll. */
  value: number;
  /** Zero-pad the displayed numeral to this many digits (BFCM style "04"). */
  pad?: number;
  /** Rendered after the numeral in the secondary color (e.g. "+", "x"). */
  suffix?: string;
  label: string;
  href?: string;
}
