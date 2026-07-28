import type { Metadata } from "next";
import Link from "next/link";

/** Old-site route kept alive for anyone holding the URL: presentations now
 * live on /papers.
 *
 * `redirect()` cannot be used here. A static export has no server to issue a
 * 3xx, so Next bakes an error shell into the HTML and only completes the
 * redirect once the client JS hydrates. A meta refresh works on a plain
 * static host and without JavaScript, and the visible link covers the rest. */
export const metadata: Metadata = {
  title: "Presentations",
  robots: { index: false, follow: true },
};

export default function PresentationsRedirect() {
  return (
    <div className="pt-12">
      <meta httpEquiv="refresh" content="0; url=/papers/" />
      <p className="text-[13px] leading-relaxed text-muted">
        Talks and presentations moved to{" "}
        <Link href="/papers" className="text-accent hover:underline">
          Research
        </Link>
        .
      </p>
    </div>
  );
}
