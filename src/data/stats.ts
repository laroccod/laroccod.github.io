/** Big-number stats for the BFCM-style StatRow. Counts derive from the data
 * arrays so they never drift from the content. */

import { PRESENTATIONS, PUBLICATIONS } from "./content";
import { getCommitCountStat } from "./github";
import type { Stat } from "./types";

const BASE_HERO_STATS: Stat[] = [
  {
    value: PUBLICATIONS.length,
    pad: 2,
    label: "Peer-reviewed publications",
    href: "/papers",
  },
  {
    value: PRESENTATIONS.length,
    pad: 2,
    label: "Talks & invited seminars",
    href: "/papers#talks",
  },
  {
    value: 11,
    pad: 2,
    label: "Courses taught as TA",
    href: "/teaching",
  },
];

/** Resolved once per build: the base counts plus the live GitHub tracker. */
export async function getHeroStats(): Promise<Stat[]> {
  return [...BASE_HERO_STATS, await getCommitCountStat()];
}

export const TEACHING_STATS: Stat[] = [
  { value: 11, pad: 2, label: "Courses as TA" },
  { value: 5, pad: 2, label: "Years teaching" },
  { value: 3, pad: 2, label: "Institutions" },
];
