"""Generate the paper figures and talk-slide previews in src/assets/.

Two pipelines, both Ghostscript + Pillow, run by hand (dev-only; neither
package exists in the Pyodide runtime):

  figures  content/figures/*.pdf|png  ->  src/assets/papers/<paper>/<name>.png
           The private figure sources are gitignored, so re-running this needs
           a local content/ checkout; the rendered PNGs are committed.

  talks    src/assets/talks/<deck>.pdf -> src/assets/talks/previews/<deck>-<n>.png
           Title slide plus a couple of hand-picked content slides per deck.

Everything is rendered oversized and downscaled to MAX_WIDTH with Lanczos:
the site ships to a static host and loads over Pyodide, so page weight
matters more than pixel-peeping a plot.

    python3 tools/build_media.py [figures|talks]
"""

import subprocess
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
FIGURES_SRC = REPO / "content" / "figures"
TALKS_DIR = REPO / "src" / "assets" / "talks"
PAPERS_OUT = REPO / "src" / "assets" / "papers"
PREVIEWS_OUT = TALKS_DIR / "previews"

RENDER_DPI = 220      # oversample, then downscale for clean edges
MAX_WIDTH = 1400      # px; plenty for the lightbox at any viewport
# Figures are line art and stay PNG. Slide previews are dense mixed-content
# pages where PNG costs ~5x what a high-quality JPEG does, and the whole site
# ships as static assets over Pyodide, so they go out as JPEG.
SLIDE_WIDTH = 1200
SLIDE_QUALITY = 82

# paper slug -> (output name, source file in content/figures/)
FIGURES: dict[str, tuple[tuple[str, str], ...]] = {
    "characterizing-hnls": (
        ("1d-e", "1D-E-Model-1.pdf"),
        ("fit-2", "Fit-2-FASER-0.6-0.1.pdf"),
        ("atlas-faser", "ATLAS-FASER.png"),
        ("lam-2", "LAM-2-FASER-0.05-0.0.pdf"),
    ),
    "simulating-hnls": (
        ("faser-pr-111", "FASERPR111.pdf"),
        ("111-brs", "111-Brs.pdf"),
    ),
}

# deck stem -> 1-based slide numbers (first entry is the title slide)
TALK_SLIDES: dict[str, tuple[int, ...]] = {
    "thesis-defense": (1, 19, 40),
    "fpf9": (1, 10, 13),
    "hnl-seminar-2025": (1, 4, 34),
    "susy-2025": (1, 11, 17),
    "aps-2025": (1, 10, 13),
    "flasy-2024": (1, 4, 7),
}


def _shrink(path: Path, width: int = MAX_WIDTH, dest: Path | None = None,
            **save_args) -> None:
    """Downscale to `width` and re-encode (in place unless `dest` is given)."""
    with Image.open(path) as im:
        im = im.convert("RGB")
        if im.width > width:
            h = round(im.height * width / im.width)
            im = im.resize((width, h), Image.LANCZOS)
        im.save(dest or path, optimize=True, **save_args)


def _render(src: Path, dest: Path, page: int = 1, dpi: int = RENDER_DPI) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["gs", "-q", "-sDEVICE=png16m", f"-r{dpi}",
         f"-dFirstPage={page}", f"-dLastPage={page}",
         "-dBATCH", "-dNOPAUSE", "-o", str(dest), str(src)],
        check=True,
    )


def build_figures() -> None:
    if not FIGURES_SRC.is_dir():
        sys.exit(f"missing {FIGURES_SRC} (private, gitignored — needs a local "
                 "content/ checkout)")
    for slug, entries in FIGURES.items():
        for name, filename in entries:
            src = FIGURES_SRC / filename
            dest = PAPERS_OUT / slug / f"{name}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            if src.suffix.lower() == ".pdf":
                # Standalone figure PDFs cropped to the ink are only ~20 pt
                # wide, so a fixed dpi renders them at thumbnail size; scale
                # the dpi to land near MAX_WIDTH instead.
                dpi = max(RENDER_DPI, round(72 * MAX_WIDTH / _pdf_width(src)))
                _render(src, dest, dpi=dpi)
            else:
                with Image.open(src) as im:
                    im.convert("RGB").save(dest)
            _shrink(dest)
            print(f"{dest.relative_to(REPO)}")


def _pdf_width(pdf: Path) -> float:
    """Page width in points, from the first MediaBox in the file."""
    raw = pdf.read_bytes()
    marker = raw.find(b"/MediaBox")
    box = raw[marker:marker + 80].split(b"[")[1].split(b"]")[0].split()
    return float(box[2]) - float(box[0])


def build_talks() -> None:
    PREVIEWS_OUT.mkdir(parents=True, exist_ok=True)
    for stem, pages in TALK_SLIDES.items():
        for page in pages:
            raw = PREVIEWS_OUT / f"{stem}-{page}.png"
            dest = raw.with_suffix(".jpg")
            _render(TALKS_DIR / f"{stem}.pdf", raw, page=page, dpi=110)
            _shrink(raw, width=SLIDE_WIDTH, dest=dest,
                    quality=SLIDE_QUALITY, subsampling=0)
            raw.unlink()
            print(f"{dest.relative_to(REPO)}")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("figures", "all"):
        build_figures()
    if which in ("talks", "all"):
        build_talks()
