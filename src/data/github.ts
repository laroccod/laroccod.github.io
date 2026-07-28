/** Build-time GitHub tracker: total commits authored by GITHUB_USER across
 * their public non-fork repos (forks share upstream history and would
 * double-count). Fetched fresh on every `next build`; the route stays static
 * because no request-time APIs are used. Falls back to the last known count
 * when the API is unreachable or rate-limited (offline builds, dev without
 * GITHUB_TOKEN). */

import type { Stat } from "./types";

const GITHUB_USER = "laroccod";

/** Last known good total (2026-07); keeps the build green when the API fails. */
const FALLBACK_COMMITS = 76;

const STATS_RETRIES = 5;
const STATS_RETRY_DELAY_MS = 2000;

interface RepoSummary {
  name: string;
  fork: boolean;
}

interface ContributorStats {
  author: { login: string } | null;
  /** Total commits by this author in the repo. */
  total: number;
}

function ghFetch(url: string): Promise<Response> {
  const token = process.env.GITHUB_TOKEN;
  return fetch(url, {
    headers: {
      accept: "application/vnd.github+json",
      ...(token ? { authorization: `Bearer ${token}` } : {}),
    },
  });
}

/** `/stats/contributors` returns 202 while GitHub computes the stats in the
 * background; poll a few times before giving up on that repo. */
async function contributorStats(
  repo: string,
): Promise<ContributorStats[] | null> {
  const url = `https://api.github.com/repos/${GITHUB_USER}/${repo}/stats/contributors`;
  for (let attempt = 0; attempt < STATS_RETRIES; attempt++) {
    const res = await ghFetch(url);
    if (res.status === 200) return res.json();
    if (res.status !== 202) return null;
    await new Promise((resolve) => setTimeout(resolve, STATS_RETRY_DELAY_MS));
  }
  return null;
}

export async function getCommitCount(): Promise<number> {
  try {
    const res = await ghFetch(
      `https://api.github.com/users/${GITHUB_USER}/repos?per_page=100`,
    );
    if (!res.ok) return FALLBACK_COMMITS;
    const repos: RepoSummary[] = await res.json();
    const perRepo = await Promise.all(
      repos.filter((r) => !r.fork).map((r) => contributorStats(r.name)),
    );
    let total = 0;
    for (const contributors of perRepo) {
      for (const c of contributors ?? []) {
        if (c.author?.login !== GITHUB_USER) continue;
        total += c.total;
      }
    }
    // Incomplete data (a repo timed out, or an empty sum) must never
    // undercount below the last known total.
    if (perRepo.some((s) => s === null) || total === 0) {
      return Math.max(total, FALLBACK_COMMITS);
    }
    return total;
  } catch {
    return FALLBACK_COMMITS;
  }
}

/** The hero-row card: "NN+ commits", linking to the GitHub profile. */
export async function getCommitCountStat(): Promise<Stat> {
  const commits = await getCommitCount();
  return {
    value: commits,
    suffix: "+",
    label: "Commits on GitHub",
    href: `https://github.com/${GITHUB_USER}`,
  };
}
