/** Build-time GitHub tracker: total commits authored by GITHUB_USER across
 * their public non-fork repos (forks share upstream history and would
 * double-count). Fetched fresh on every `next build`; the route stays static
 * because no request-time APIs are used. Falls back to the last known count
 * when the API is unreachable or rate-limited (offline builds, dev without
 * GITHUB_TOKEN). */

import type { Stat } from "./types";

const GITHUB_USER = "laroccod";

/** Last known good total (2026-07-28, resolved from the API); keeps the build
 * green when the API fails. Refresh it when the build log reports a higher
 * resolved count. */
const FALLBACK_COMMITS = 78;

/** `/stats/contributors` answers 202 until GitHub has computed the stats.
 * A cold cache on a CI runner needs noticeably longer than a warm one on a
 * machine that has browsed the repos recently, and the first deploy of this
 * site fell back for exactly that reason. Repos are polled concurrently, so
 * the budget below costs at most ~30s of wall clock, not 30s per repo. */
const STATS_RETRIES = 20;
const STATS_RETRY_DELAY_MS = 3000;

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
 * background; poll until the budget runs out before giving up on that repo.
 * Names the repo and the reason on stdout so a fallback is diagnosable from
 * the build log rather than just being a number that looks plausible. */
async function contributorStats(
  repo: string,
): Promise<ContributorStats[] | null> {
  const url = `https://api.github.com/repos/${GITHUB_USER}/${repo}/stats/contributors`;
  for (let attempt = 0; attempt < STATS_RETRIES; attempt++) {
    const res = await ghFetch(url);
    if (res.status === 200) {
      const stats: ContributorStats[] = await res.json();
      // A 200 with an empty body means "computed, but nothing to report",
      // which for a repo the user has committed to means it is still warming.
      if (stats.length > 0) return stats;
      if (attempt === STATS_RETRIES - 1) {
        console.log(`[github] ${repo}: empty stats after ${attempt + 1} tries`);
        return null;
      }
    } else if (res.status !== 202) {
      console.log(`[github] ${repo}: HTTP ${res.status}, giving up`);
      return null;
    }
    await new Promise((resolve) => setTimeout(resolve, STATS_RETRY_DELAY_MS));
  }
  console.log(`[github] ${repo}: still computing after ${STATS_RETRIES} tries`);
  return null;
}

/** The fallback is deliberately plausible, so a failed fetch is invisible on
 * the page. Every outcome is therefore announced on stdout, which is the only
 * way to tell a real count that happens to equal FALLBACK_COMMITS from an
 * actual fallback. Grep the build log (or the Actions run) for "[github]". */
function report(count: number, source: "api" | "fallback", why = ""): number {
  const detail = source === "api" ? "resolved from the API" : `FELL BACK${why}`;
  console.log(`[github] commit count ${count} (${detail})`);
  return count;
}

export async function getCommitCount(): Promise<number> {
  try {
    const res = await ghFetch(
      `https://api.github.com/users/${GITHUB_USER}/repos?per_page=100`,
    );
    if (!res.ok) {
      return report(FALLBACK_COMMITS, "fallback", `: repo list HTTP ${res.status}`);
    }
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
    const missing = perRepo.filter((s) => s === null).length;
    if (missing > 0 || total === 0) {
      return report(
        Math.max(total, FALLBACK_COMMITS),
        "fallback",
        `: ${missing} of ${perRepo.length} repos returned no stats, partial total ${total}`,
      );
    }
    return report(total, "api");
  } catch (err) {
    const why = err instanceof Error ? `: ${err.message}` : "";
    return report(FALLBACK_COMMITS, "fallback", why);
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
