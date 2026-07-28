export function Chip({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-block border border-line bg-surface px-2 py-0.5 text-xs text-muted">
      {children}
    </span>
  );
}
