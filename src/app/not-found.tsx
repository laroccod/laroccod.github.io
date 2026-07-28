import type { Metadata } from "next";
import { MatrixRain } from "@/components/hero/MatrixRain";
import { LinkButton } from "@/components/ui/LinkButton";

export const metadata: Metadata = {
  title: "404 · Signal lost",
  description: "This page does not exist.",
};

export default function NotFound() {
  return (
    <section className="relative -mx-5 flex min-h-[70vh] items-center overflow-hidden px-5 sm:-mx-8 sm:px-8">
      <MatrixRain className="absolute inset-0 h-full w-full opacity-40" />
      {/* Same readability scrim treatment as the hero */}
      <div
        aria-hidden
        className="absolute inset-0"
        style={{
          background:
            "radial-gradient(ellipse at center, color-mix(in srgb, var(--bg) 88%, transparent) 0%, color-mix(in srgb, var(--bg) 55%, transparent) 60%, transparent 100%)",
        }}
      />
      <div className="relative mx-auto max-w-xl py-20 text-center">
        <p className="kicker !text-accent">
          ▸▸ SIGNAL LOST <span aria-hidden>{"//"}</span> NO CARRIER
        </p>
        <p
          className="glitch stat-numeral mt-6 text-[96px] font-bold sm:text-[128px]"
          data-text="404"
        >
          404
        </p>
        <p className="mt-6 text-[14px] leading-relaxed text-muted">
          The requested route scattered outside the detector acceptance.
          Nothing was reconstructed at this address.
        </p>
        <div className="mt-8 flex justify-center">
          <LinkButton href="/" external={false} variant="primary">
            Return to base
          </LinkButton>
        </div>
      </div>
    </section>
  );
}
