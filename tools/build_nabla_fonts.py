"""Generate the themed Nabla display fonts in src/assets/fonts/nabla/.

Nabla (github.com/google/fonts, OFL) is a COLRv1 color font: its colors live
in the CPAL table, so each site palette gets its own build with the palette
rewritten, plus a "glint" build (every color blended toward white) that the
hero shimmer sweeps across the name.

Pipeline per theme: instance the variable font at EDPT=180 (extrusion depth)
and EHLT=12 (edge highlight), rewrite CPAL palette 0, subset to printable
ASCII (the font only ever renders the name and the DLR brand), save.

Run with fonttools installed and Nabla[EDPT,EHLT].ttf next to this script:
    curl -sLO https://github.com/google/fonts/raw/main/ofl/nabla/Nabla%5BEDPT%2CEHLT%5D.ttf
    python3 tools/build_nabla_fonts.py

CPAL entry roles (10 entries): 1 darkest extrusion shadow, 2-3 extrusion
sides, 0/4/6 face, 5/7 light face, 8 lighter, 9 top highlight.
"""

import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.C_P_A_L_ import Color
from fontTools.varLib.instancer import instantiateVariableFont

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
import theme  # noqa: E402  (the palette registry)

VAR_FONT = Path(__file__).parent / "Nabla[EDPT,EHLT].ttf"
OUT_DIR = REPO / "src" / "assets" / "fonts" / "nabla"

AXES = {"EDPT": 180, "EHLT": 12}
GLINT_BLEND = 0.55  # fraction toward white for the shimmer build
SUBSET_UNICODES = "U+0020-007E"  # printable ASCII: name + brand + headroom


def blend(hexcol: str, toward: tuple, t: float) -> str:
    r, g, b = (int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    r = round(r + (toward[0] - r) * t)
    g = round(g + (toward[1] - g) * t)
    b = round(b + (toward[2] - b) * t)
    return f"#{r:02X}{g:02X}{b:02X}"


def lighten(c, t):
    return blend(c, (255, 255, 255), t)


def darken(c, t):
    return blend(c, (0, 0, 0), t)


def palette_for(name: str, t: dict) -> list[str]:
    """10 CPAL colors for a theme, hand-tuned or derived from its palette."""
    # Hand-approved builds (kept verbatim).
    if name == "lavender":
        return ["#7C6BD6", "#4C3D9E", "#6A59C4", "#6150BA", "#7C6BD6",
                "#A99CEA", "#7C6BD6", "#A99CEA", "#D3CBF6", "#FFFFFF"]
    if name == "neon_gold":
        return ["#FAEB92", "#5E3D85", "#8F6DB0", "#9A78BB", "#FAEB92",
                "#FCF4B6", "#FAEB92", "#FCF4B6", "#FEFBDA", "#FFFFFF"]
    if name == "prism":
        # Magenta face over the palette's azure counterpoint: the derived
        # on_surface_variant extrusion reads muddy next to the hot accent.
        return ["#FF006E", "#1A3C7A", "#2757B8", "#2E66D6", "#FF006E",
                "#FF4D97", "#FF006E", "#FF4D97", "#FFA3C8", "#FFFFFF"]
    accent = t["accent"]
    if t["mode"] == "light":
        # Monochrome accent ramp (the approved lavender recipe).
        return [accent, darken(accent, 0.35), darken(accent, 0.13),
                darken(accent, 0.22), accent, lighten(accent, 0.35),
                accent, lighten(accent, 0.35), lighten(accent, 0.68),
                "#FFFFFF"]
    # Dark themes: accent face over a muted counterpoint extrusion
    # (the approved neon-gold recipe, extrusion from on_surface_variant).
    osv = t["on_surface_variant"]
    return [accent, darken(osv, 0.45), darken(osv, 0.18),
            darken(osv, 0.10), accent, lighten(accent, 0.30),
            accent, lighten(accent, 0.30), lighten(accent, 0.60),
            "#FFFFFF"]


def set_palette(font: TTFont, colors: list[str]) -> None:
    pal = font["CPAL"].palettes[0]
    for i, hexcol in enumerate(colors):
        pal[i] = Color(red=int(hexcol[1:3], 16), green=int(hexcol[3:5], 16),
                       blue=int(hexcol[5:7], 16), alpha=pal[i].alpha)


def subset_ascii(font: TTFont) -> TTFont:
    # Drop the OT-SVG fallback: Flutter/CanvasKit renders the COLRv1 table
    # (the CPAL rewrite visibly recolors it), and SVG subsetting needs lxml.
    if "SVG " in font:
        del font["SVG "]
    options = subset.Options()
    options.unicodes = subset.parse_unicodes(SUBSET_UNICODES)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=options.unicodes)
    subsetter.subset(font)
    # Round-trip through bytes so table offsets are rebuilt cleanly.
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    return TTFont(buf)


def build(name: str, colors: list[str], out: Path) -> None:
    font = TTFont(VAR_FONT)
    instantiateVariableFont(font, AXES, inplace=True)
    set_palette(font, colors)
    font = subset_ascii(font)
    out.parent.mkdir(parents=True, exist_ok=True)
    font.save(out)
    print(f"wrote {out.relative_to(REPO)} ({out.stat().st_size // 1024} KB)")


def main() -> None:
    if not VAR_FONT.exists():
        raise SystemExit(f"missing {VAR_FONT.name}; see module docstring")
    for name, t in theme.THEMES.items():
        colors = palette_for(name, t)
        build(name, colors, OUT_DIR / f"{name}.ttf")
        glint = [lighten(c, GLINT_BLEND) for c in colors]
        build(name, glint, OUT_DIR / f"{name}_glint.ttf")


if __name__ == "__main__":
    main()
