interface StatusChipProps {
  tone?: "accent" | "secondary";
  children: React.ReactNode;
}

/** Terminal status readout: pulsing square LED + uppercase label,
 * e.g. `▪ ONLINE`. The dot inherits the tone color via currentColor. */
export function StatusChip({ tone = "accent", children }: StatusChipProps) {
  return (
    <span
      className={`kicker inline-flex items-center gap-2 ${
        tone === "accent" ? "!text-accent" : "!text-secondary"
      }`}
    >
      <span className="status-dot" aria-hidden />
      {children}
    </span>
  );
}
