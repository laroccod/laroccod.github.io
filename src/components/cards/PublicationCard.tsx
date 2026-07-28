import { AbstractDisclosure } from "@/components/ui/AbstractDisclosure";
import { FigureStrip } from "@/components/ui/FigureStrip";
import { LinkButton } from "@/components/ui/LinkButton";
import type { Publication } from "@/data/types";

export function PublicationCard({ pub }: { pub: Publication }) {
  return (
    <article className="terminal-card p-5 sm:p-6">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <span className="kicker !text-accent">{pub.year}</span>
        <span className="kicker">{pub.venue}</span>
      </div>
      <h3 className="mt-2 text-[16px] font-bold leading-snug">{pub.title}</h3>
      <p className="mt-1 text-[13px] text-muted">{pub.authors}</p>
      <div className="mt-3">
        <LinkButton href={pub.url}>View</LinkButton>
      </div>
      {pub.abstract && <AbstractDisclosure text={pub.abstract} />}
      {pub.figures && pub.figures.length > 0 && (
        <FigureStrip figures={pub.figures} />
      )}
    </article>
  );
}
