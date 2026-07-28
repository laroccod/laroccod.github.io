interface TerminalCardProps {
  label?: string;
  className?: string;
  children: React.ReactNode;
}

export function TerminalCard({ label, className, children }: TerminalCardProps) {
  return (
    <section className={`terminal-card ${className ?? ""}`}>
      {label && (
        <div className="flex items-center gap-2 border-b border-line px-5 py-2">
          <span className="text-accent text-[11px]" aria-hidden>
            ┌─
          </span>
          <span className="kicker !text-accent">{label}</span>
          <span
            className="flex-1 border-t border-dashed border-line"
            aria-hidden
          />
        </div>
      )}
      <div className="p-5 sm:p-6">{children}</div>
    </section>
  );
}
