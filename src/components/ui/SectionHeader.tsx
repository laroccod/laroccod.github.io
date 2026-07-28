interface SectionHeaderProps {
  index: number;
  kicker: string;
  title: string;
}

export function SectionHeader({ index, kicker, title }: SectionHeaderProps) {
  return (
    <div className="mb-8">
      <p className="kicker">
        <span className="text-accent" aria-hidden>
          ▸▸{" "}
        </span>
        <span className="text-accent">
          SECTION {String(index).padStart(2, "0")}
        </span>{" "}
        <span aria-hidden>{"//"}</span> {kicker}
      </p>
      <h2 className="mt-2 text-[26px] font-bold leading-tight sm:text-3xl">
        {title}
      </h2>
      <div className="rule-fade mt-4" aria-hidden />
    </div>
  );
}
