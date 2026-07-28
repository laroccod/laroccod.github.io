import type { Metadata } from "next";
import { PublicationCard } from "@/components/cards/PublicationCard";
import { TalkCard } from "@/components/cards/TalkCard";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { PRESENTATIONS, PUBLICATIONS } from "@/data/content";

export const metadata: Metadata = {
  title: "Research",
  description:
    "Peer-reviewed publications and conference talks: heavy neutral lepton " +
    "phenomenology at forward LHC experiments, and computational biophysics.",
};

export default function PapersPage() {
  return (
    <div className="pt-12">
      <SectionHeader index={2} kicker="PAPERS & TALKS" title="Research" />

      <p className="max-w-2xl text-[13px] leading-relaxed text-muted">
        Peer-reviewed publications in particle physics phenomenology and
        computational biophysics, with selected figures from each paper.
      </p>
      <div className="mt-6 space-y-6">
        {PUBLICATIONS.map((pub) => (
          <PublicationCard key={pub.title} pub={pub} />
        ))}
      </div>

      <h3 id="talks" className="kicker !text-accent mt-14 mb-2 scroll-mt-24">
        ▸ Conference talks & seminars
      </h3>
      <p className="max-w-2xl text-[13px] leading-relaxed text-muted">
        Contributed talks, invited seminars, and the thesis defense, with
        slides and selected preview frames.
      </p>
      <div className="mt-6 space-y-6">
        {PRESENTATIONS.map((talk) => (
          <TalkCard key={`${talk.date}-${talk.event}`} talk={talk} />
        ))}
      </div>
    </div>
  );
}
