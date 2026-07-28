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
const FALLBACK_COMMITS = 92;

interface RepoSummary {
  name: string;
  fork: boolean;
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

/** Commits authored by GITHUB_USER on one repo's default branch.
 *
 * Asks for a single commit and reads the pagination Link header, whose last
 * page number equals the commit count. This answers immediately, which is why
 * it replaced `/stats/contributors`: that endpoint returns 202 while GitHub
 * recomputes in the background, and a push invalidates the pushed repo's
 * stats, so a build triggered by a push to this very repo always found its own
 * stats unavailable no matter how long it waited. Polling long enough to
 * matter also blew past Next's 60s per-page build timeout. */
async function commitsInRepo(repo: string): Promise<number | null> {
  const url =
    `https://api.github.com/repos/${GITHUB_USER}/${repo}/commits` +
    `?author=${GITHUB_USER}&per_page=1`;
  // Author-filtered commit queries are expensive for GitHub to serve, and
  // firing them off concurrently reliably drew 504s. They are issued one at a
  // time (see getCommitCount) and retried with a growing pause on the
  // gateway errors and rate-limit responses that remain.
  let res = await ghFetch(url);
  for (
    let attempt = 0;
    attempt < 3 && (res.status >= 500 || res.status === 403 || res.status === 429);
    attempt++
  ) {
    await new Promise((resolve) => setTimeout(resolve, 1000 * 2 ** attempt));
    res = await ghFetch(url);
  }
  // 409 is an empty repository, which is a real answer of zero.
  if (res.status === 409) return 0;
  if (!res.ok) {
    console.log(`[github] ${repo}: HTTP ${res.status}`);
    return null;
  }
  const last = res.headers.get("link")?.match(/[?&]page=(\d+)>;\s*rel="last"/);
  if (last) return Number(last[1]);
  // No Link header means the result fits on one page: zero or one commit.
  const commits: unknown = await res.json();
  return Array.isArray(commits) ? commits.length : null;
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
      return report(
        FALLBACK_COMMITS,
        "fallback",
        `: repo list HTTP ${res.status}`,
      );
    }
    const repos: RepoSummary[] = await res.json();
    // Sequential on purpose: concurrent author-filtered queries draw 504s.
    // A handful of repos costs a couple of seconds.
    const perRepo: (number | null)[] = [];
    for (const repo of repos.filter((r) => !r.fork)) {
      perRepo.push(await commitsInRepo(repo.name));
    }
    const missing = perRepo.filter((n) => n === null).length;
    const total = perRepo.reduce((sum: number, n) => sum + (n ?? 0), 0);
    // Incomplete data (a repo errored, or an empty sum) must never undercount
    // below the last known total.
    if (missing > 0 || total === 0) {
      return report(
        Math.max(total, FALLBACK_COMMITS),
        "fallback",
        `: ${missing} of ${perRepo.length} repos did not answer, partial total ${total}`,
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
