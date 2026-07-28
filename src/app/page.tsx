import Image from "next/image";
import { MatrixRain } from "@/components/hero/MatrixRain";
import { ThesisDiagram } from "@/components/hero/ThesisDiagram";
import { Wordmark } from "@/components/hero/Wordmark";
import { AbstractDisclosure } from "@/components/ui/AbstractDisclosure";
import { TypedText } from "@/components/ui/TypedText";
import { FigureStrip } from "@/components/ui/FigureStrip";
import { LinkButton } from "@/components/ui/LinkButton";
import { StatRow } from "@/components/ui/StatCard";
import { TerminalCard } from "@/components/ui/TerminalCard";
import {
  DEFENSE_SLIDES,
  LOCATION,
  NAME,
  SUMMARY,
  TAGLINE,
  THESIS_ABSTRACT,
  THESIS_BLURB,
  THESIS_FIGURES,
  THESIS_TITLE,
  THESIS_URL,
  TITLE,
} from "@/data/content";
import { getHeroStats } from "@/data/stats";

export default async function HomePage() {
  const heroStats = await getHeroStats();
  return (
    <>
      {/* Hero with the physics-glyph rain band behind it */}
      <section className="relative -mx-5 overflow-hidden px-5 pb-12 pt-14 sm:-mx-8 sm:px-8 sm:pt-20">
        <MatrixRain className="absolute inset-0 h-full w-full opacity-40" />
        {/* Readability scrim: quiets the rain behind the hero text */}
        <div
          aria-hidden
          className="absolute inset-0"
          style={{
            background:
              "linear-gradient(to right, color-mix(in srgb, var(--bg) 90%, transparent) 0%, color-mix(in srgb, var(--bg) 82%, transparent) 52%, transparent 75%)",
          }}
        />
        <div className="relative flex flex-col-reverse items-start gap-8 sm:flex-row sm:items-center sm:gap-14">
          <div className="max-w-xl">
            <p className="kicker !text-accent">
              ▸▸ {LOCATION} <span aria-hidden>{"//"}</span> ONLINE
            </p>
            <h1 className="mt-3 text-4xl font-bold leading-tight sm:text-[52px]">
              <Wordmark text={NAME} />
            </h1>
            <p className="mt-3 text-[15px] font-bold text-accent">{TITLE}</p>
            <p className="mt-4 text-[14px] leading-relaxed text-muted">
              <TypedText
                text={TAGLINE}
                speed={4000 / TAGLINE.length}
                startDelay={400}
                keepCursor
              />
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <LinkButton href="/projects" variant="primary" external={false}>
                View projects
              </LinkButton>
              <LinkButton href="/contact" external={false}>
                Get in touch
              </LinkButton>
            </div>
          </div>
          <div className="figure-frame shrink-0">
            <Image
              src="/headshot.jpg"
              alt={`Portrait of ${NAME}`}
              width={260}
              height={260}
              priority
              className="block w-[200px] object-cover sm:w-[260px]"
              style={{ height: "auto" }}
            />
          </div>
        </div>
      </section>

      {/* BFCM-style stat row */}
      <section className="mt-2">
        <StatRow stats={heroStats} />
      </section>

      {/* About */}
      <section className="mt-12">
        <TerminalCard label="ABOUT">
          <p className="text-[14px] leading-relaxed">{SUMMARY}</p>
        </TerminalCard>
      </section>

      {/* Thesis */}
      <section className="mt-8">
        <TerminalCard label="PH.D. THESIS">
          <h2 className="text-[17px] font-bold leading-snug">{THESIS_TITLE}</h2>
          <p className="mt-3 text-[13px] leading-relaxed text-muted">
            {THESIS_BLURB}
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            <LinkButton href={THESIS_URL}>Read on eScholarship</LinkButton>
            <LinkButton href={DEFENSE_SLIDES} external>
              Defense slides (PDF)
            </LinkButton>
          </div>
          <AbstractDisclosure text={THESIS_ABSTRACT} />
          <ThesisDiagram />
          <FigureStrip figures={THESIS_FIGURES} />
        </TerminalCard>
      </section>
    </>
  );
}
