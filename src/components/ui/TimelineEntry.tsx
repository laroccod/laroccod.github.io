interface TimelineEntryProps {
  role: string;
  org: string;
  dates: string;
  subtitle?: string;
  bullets: string[];
}

export function TimelineEntry({
  role,
  org,
  dates,
  subtitle,
  bullets,
}: TimelineEntryProps) {
  return (
    <div className="terminal-card p-5 sm:p-6">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <h3 className="text-[16px] font-bold">{role}</h3>
        <span className="kicker !text-accent">{dates}</span>
      </div>
      <p className="mt-1 text-[13px] text-muted">{org}</p>
      {subtitle && <p className="text-[13px] italic text-muted">{subtitle}</p>}
      <ul className="mt-3 space-y-2">
        {bullets.map((bullet) => (
          <li key={bullet} className="flex gap-2 text-[13px] leading-relaxed">
            <span className="text-accent" aria-hidden>
              ▸
            </span>
            <span>{bullet}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
