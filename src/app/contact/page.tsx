import type { Metadata } from "next";
import { MatrixRain } from "@/components/hero/MatrixRain";
import { ContactCard } from "@/components/cards/ContactCard";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { StatusChip } from "@/components/ui/StatusChip";
import { TerminalCard } from "@/components/ui/TerminalCard";
import { TypedText } from "@/components/ui/TypedText";
import { CONTACT_LINKS, EMAIL, LOCATION } from "@/data/content";
import { ogMeta } from "@/lib/og-cards";

export const metadata: Metadata = {
  title: "Contact",
  description: "Email, GitHub, LinkedIn, and ORCID.",
  ...ogMeta("contact"),
};

/** Decorative ping replies staged in after the typed command finishes. The
 * host is derived from EMAIL so the replies cannot drift away from the
 * address actually being pinged. */
const EMAIL_HOST = EMAIL.split("@")[1];

const REPLY_LINES = [
  `64 bytes from ${EMAIL_HOST}: seq=0 time=0.42 ms`,
  `64 bytes from ${EMAIL_HOST}: seq=1 time=0.38 ms`,
  "-- link established: email is the fastest channel --",
];

export default function ContactPage() {
  return (
    <div className="relative pt-12">
      <SectionHeader index={5} kicker="TRANSMISSION" title="Contact" />

      <p className="max-w-2xl text-[13px] leading-relaxed text-muted">
        Based in {LOCATION}. The fastest way to reach me is email; everything
        else below links to a public profile.
      </p>
      <div className="mt-4">
        <StatusChip>Online</StatusChip>
      </div>

      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        {CONTACT_LINKS.map((link) => (
          <ContactCard key={link.label} link={link} />
        ))}
      </div>

      <div className="mt-8">
        <TerminalCard label="UPLINK">
          <div className="font-mono text-[13px] leading-relaxed">
            <TypedText
              text={`$ ping ${EMAIL}`}
              speed={26}
              startDelay={350}
              className="text-ink"
            />
            {REPLY_LINES.map((line, i) => (
              <p
                key={line}
                className="uplink-reply text-muted"
                style={{ "--delay": `${1500 + i * 350}ms` } as React.CSSProperties}
              >
                {line}
              </p>
            ))}
          </div>
        </TerminalCard>
      </div>

      <div className="relative mt-12 h-48 overflow-hidden">
        <MatrixRain className="absolute inset-0 h-full w-full opacity-40" />
      </div>
    </div>
  );
}
