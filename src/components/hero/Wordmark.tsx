interface WordmarkProps {
  text: string;
  className?: string;
}

/** Hero name: per-letter wave on mount/hover with a glint sweep across the
 * word. Letters are aria-hidden; a visually-hidden span carries the name. */
export function Wordmark({ text, className }: WordmarkProps) {
  return (
    <span className={`wordmark inline-block ${className ?? ""}`}>
      <span className="sr-only">{text}</span>
      <span aria-hidden>
        {Array.from(text).map((letter, i) => (
          <span
            // eslint-disable-next-line react/no-array-index-key
            key={i}
            className="wordmark-letter"
            style={{ "--letter-index": i } as React.CSSProperties}
          >
            {letter === " " ? " " : letter}
          </span>
        ))}
      </span>
    </span>
  );
}
