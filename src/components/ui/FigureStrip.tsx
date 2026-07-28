"use client";

import Image from "next/image";
import { useRef, useState } from "react";
import type { Figure } from "@/data/types";

interface FigureStripProps {
  figures: Figure[];
  /** Thumbnail row height in px. */
  height?: number;
  caption?: string;
  /** White mat behind each figure. Right for black-on-white paper line
   * art, wrong for app screenshots, which bring their own background and
   * would just gain a white ring. */
  matted?: boolean;
}

/** Wrapping row of white-matted figure thumbnails; click opens a native
 * <dialog> lightbox with the full image and caption. */
export function FigureStrip({
  figures,
  height,
  caption = "Select figures. Click one to enlarge.",
  matted = true,
}: FigureStripProps) {
  const mat = matted ? "figure-mat" : undefined;
  const dialogRef = useRef<HTMLDialogElement>(null);
  const [active, setActive] = useState<Figure | null>(null);
  // Shrink thumbs when there are many so a row doesn't strand an orphan
  const thumbHeight = height ?? (figures.length > 3 ? 118 : 150);

  const open = (figure: Figure) => {
    setActive(figure);
    dialogRef.current?.showModal();
  };

  return (
    <div className="mt-4">
      <div className="flex flex-wrap gap-3">
        {figures.map((figure) => (
          <button
            key={figure.src}
            type="button"
            onClick={() => open(figure)}
            className="figure-frame max-w-full shrink-0 hover:scale-[1.04] focus-visible:outline focus-visible:outline-accent"
            aria-label={`Enlarge figure: ${figure.caption.slice(0, 80)}`}
          >
            <div className={mat}>
              <Image
                src={figure.src}
                alt={figure.caption}
                width={Math.round(thumbHeight * 1.5)}
                height={thumbHeight}
                className="max-w-full object-contain"
                style={{ height: thumbHeight, width: "auto" }}
                sizes="(max-width: 640px) 90vw, 400px"
              />
            </div>
          </button>
        ))}
      </div>
      <p className="kicker mt-2 !text-[11px]">{caption}</p>

      <dialog
        ref={dialogRef}
        onClick={(e) => {
          if (e.target === dialogRef.current) dialogRef.current?.close();
        }}
        className="m-auto max-h-[92vh] max-w-[92vw] border border-line-bright bg-panel p-0 text-ink backdrop:bg-black/80"
      >
        {active && (
          <div className="flex flex-col">
            <div className={mat}>
              {/* Full-size view: plain img keeps natural dimensions */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={active.src}
                alt={active.caption}
                className="max-h-[70vh] w-auto max-w-full object-contain"
              />
            </div>
            <div className="flex items-start justify-between gap-4 p-4">
              <p className="text-[13px] leading-relaxed text-muted">
                {active.caption}
              </p>
              <button
                type="button"
                onClick={() => dialogRef.current?.close()}
                className="shrink-0 text-[13px] text-muted hover:text-accent"
              >
                [ close ]
              </button>
            </div>
          </div>
        )}
      </dialog>
    </div>
  );
}
