import type { Metadata } from "next";
import { Chip } from "@/components/ui/Chip";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { StatRow } from "@/components/ui/StatCard";
import { TerminalCard } from "@/components/ui/TerminalCard";
import { TimelineEntry } from "@/components/ui/TimelineEntry";
import {
  COURSES_PREPARED,
  MENTORING,
  TEACHING_PROFILE,
  TEACHING_ROLES,
} from "@/data/content";
import { TEACHING_STATS } from "@/data/stats";
import { ogMeta } from "@/lib/og-cards";

export const metadata: Metadata = {
  title: "Teaching",
  description:
    "Teaching assistant and tutoring experience across 11 physics courses, " +
    "plus mentoring and outreach.",
  ...ogMeta("teaching"),
};

export default function TeachingPage() {
  return (
    <div className="pt-12">
      <SectionHeader index={3} kicker="INSTRUCTION" title="Teaching" />

      <TerminalCard label="PROFILE">
        <p className="text-[14px] leading-relaxed">{TEACHING_PROFILE}</p>
      </TerminalCard>

      <div className="mt-6">
        <StatRow stats={TEACHING_STATS} />
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">▸ Teaching roles</h3>
      <div className="space-y-4">
        {TEACHING_ROLES.map((role) => (
          <TimelineEntry
            key={`${role.role}-${role.org}`}
            role={role.role}
            org={role.org}
            dates={role.dates}
            bullets={role.bullets}
          />
        ))}
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">▸ Courses prepared</h3>
      <div className="space-y-4">
        {COURSES_PREPARED.map((group) => (
          <TerminalCard key={group.name} label={group.name.toUpperCase()}>
            <div className="flex flex-wrap gap-2">
              {group.items.map((item) => (
                <Chip key={item}>{item}</Chip>
              ))}
            </div>
          </TerminalCard>
        ))}
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">
        ▸ Mentoring & outreach
      </h3>
      <TerminalCard>
        <ul className="space-y-2">
          {MENTORING.map((item) => (
            <li key={item} className="flex gap-2 text-[13px] leading-relaxed">
              <span className="text-accent" aria-hidden>
                ▸
              </span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </TerminalCard>
    </div>
  );
}
