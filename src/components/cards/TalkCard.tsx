import { Chip } from "@/components/ui/Chip";
import { FigureStrip } from "@/components/ui/FigureStrip";
import { LinkButton } from "@/components/ui/LinkButton";
import type { Presentation } from "@/data/types";

export function TalkCard({ talk }: { talk: Presentation }) {
  return (
    <article className="terminal-card p-5 sm:p-6">
      <div className="flex flex-wrap items-center gap-3">
        <span className="kicker !text-accent">{talk.date}</span>
        <Chip>{talk.kind}</Chip>
      </div>
      <h3 className="mt-2 text-[15px] font-bold leading-snug">{talk.title}</h3>
      <p className="mt-1 text-[13px] text-muted">
        {talk.event} · {talk.where}
      </p>
      <div className="mt-3 flex flex-wrap gap-2">
        {talk.url && <LinkButton href={talk.url}>Event page</LinkButton>}
        {talk.slides && (
          <LinkButton href={talk.slides} external>
            Slides (PDF)
          </LinkButton>
        )}
      </div>
      {talk.previews && talk.previews.length > 0 && (
        <FigureStrip
          figures={talk.previews.map((src, i) => ({
            src,
            caption: `${talk.title} (slide preview ${i + 1})`,
          }))}
          height={150}
          caption="Selected slides. Click one to enlarge."
        />
      )}
    </article>
  );
}
