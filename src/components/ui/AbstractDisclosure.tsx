interface AbstractDisclosureProps {
  text: string;
  label?: string;
}

/** Native <details> for zero-JS keyboard accessibility. */
export function AbstractDisclosure({
  text,
  label = "abstract",
}: AbstractDisclosureProps) {
  return (
    <details className="group mt-3">
      <summary className="cursor-pointer list-none text-[13px] tracking-wide text-muted transition-colors hover:text-accent">
        <span className="group-open:hidden">[ + Show {label} ]</span>
        <span className="hidden group-open:inline">[ − Hide {label} ]</span>
      </summary>
      <p className="mt-3 border-l-2 border-accent pl-4 text-[13px] leading-relaxed text-muted">
        {text}
      </p>
    </details>
  );
}
