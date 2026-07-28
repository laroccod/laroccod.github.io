import type { Metadata } from "next";
import { Chip } from "@/components/ui/Chip";
import { LinkButton } from "@/components/ui/LinkButton";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { TerminalCard } from "@/components/ui/TerminalCard";
import { TimelineEntry } from "@/components/ui/TimelineEntry";
import {
  EDUCATION,
  EXPERIENCE,
  PRESENTATIONS,
  PUBLICATIONS,
  SKILLS,
  SUMMARY,
  TEACHING,
} from "@/data/content";

export const metadata: Metadata = {
  title: "CV",
  description:
    "Curriculum vitae: research experience, education, technical skills, " +
    "publications, talks, and teaching.",
};

export default function CvPage() {
  return (
    <div className="pt-12">
      <SectionHeader index={1} kicker="CURRICULUM VITAE" title="CV" />

      <TerminalCard label="SUMMARY">
        <p className="text-[14px] leading-relaxed">{SUMMARY}</p>
      </TerminalCard>

      <h3 className="kicker !text-accent mt-10 mb-4">▸ Research experience</h3>
      <div className="space-y-4">
        {EXPERIENCE.map((exp) => (
          <TimelineEntry
            key={`${exp.role}-${exp.org}`}
            role={exp.role}
            org={exp.org}
            dates={exp.dates}
            subtitle={exp.advisor}
            bullets={exp.bullets}
          />
        ))}
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">▸ Education</h3>
      <div className="space-y-4">
        {EDUCATION.map((edu) => (
          <TimelineEntry
            key={edu.school}
            role={edu.school}
            org={edu.degree}
            dates={edu.dates}
            bullets={edu.details}
          />
        ))}
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">▸ Technical skills</h3>
      <div className="space-y-4">
        {SKILLS.map((group) => (
          <TerminalCard key={group.name} label={group.name.toUpperCase()}>
            <div className="flex flex-wrap gap-2">
              {group.items.map((item) => (
                <Chip key={item}>{item}</Chip>
              ))}
            </div>
          </TerminalCard>
        ))}
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">▸ Publications</h3>
      <div className="space-y-4">
        {PUBLICATIONS.map((pub) => (
          <TerminalCard key={pub.title}>
            <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
              <span className="kicker !text-accent">{pub.year}</span>
              <span className="kicker">{pub.venue}</span>
            </div>
            <p className="mt-2 text-[14px] font-bold leading-snug">
              {pub.title}
            </p>
            <p className="mt-1 text-[13px] text-muted">{pub.authors}</p>
            <div className="mt-3">
              <LinkButton href={pub.url}>View</LinkButton>
            </div>
          </TerminalCard>
        ))}
      </div>

      <h3 className="kicker !text-accent mt-10 mb-4">
        ▸ Talks & invited seminars
      </h3>
      <TerminalCard>
        <ul className="space-y-3">
          {PRESENTATIONS.map((talk) => (
            <li
              key={`${talk.date}-${talk.event}`}
              className="flex gap-3 text-[13px] leading-relaxed"
            >
              <span className="kicker !text-accent shrink-0 pt-0.5">
                {talk.date}
              </span>
              <span>
                {talk.title} · {talk.event}, {talk.where}
              </span>
            </li>
          ))}
        </ul>
      </TerminalCard>

      <h3 className="kicker !text-accent mt-10 mb-4">
        ▸ Teaching, service & outreach
      </h3>
      <TerminalCard>
        <ul className="space-y-2">
          {TEACHING.map((item) => (
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
