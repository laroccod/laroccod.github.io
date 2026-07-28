interface LinkButtonProps {
  href: string;
  children: React.ReactNode;
  variant?: "primary" | "ghost";
  external?: boolean;
  download?: boolean;
}

export function LinkButton({
  href,
  children,
  variant = "ghost",
  external,
  download,
}: LinkButtonProps) {
  const isExternal = external ?? /^(https?:|mailto:)/.test(href);
  const base =
    "inline-flex items-center gap-1.5 border px-3 py-1.5 text-[13px] tracking-wide transition-colors";
  const styles =
    variant === "primary"
      ? "border-accent bg-accent text-bg font-bold hover:bg-transparent hover:text-accent"
      : "border-line text-muted hover:border-line-bright hover:text-accent";
  return (
    <a
      href={href}
      className={`${base} ${styles}`}
      {...(isExternal && !href.startsWith("mailto:")
        ? { target: "_blank", rel: "noopener noreferrer" }
        : {})}
      {...(download ? { download: true } : {})}
    >
      <span aria-hidden>[</span>
      {children}
      {isExternal && <span aria-hidden>↗</span>}
      <span aria-hidden>]</span>
    </a>
  );
}
