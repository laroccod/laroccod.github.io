"""Site theme: the labforge palette registry.

The framework this site showcases ships a small table of hand-tuned palettes;
the site carries a curated set: labforge's paper, neon gold, mint and lavender
plus three custom palettes built from coolors.co seeds (ember, olive, prism).
It runs the same design system, and the navbar theme picker lets a visitor
switch between them.

Every view and component reads the module-level colour constants (``ACCENT``,
``SURFACE``, ...) at build time. ``apply(name)`` rebinds those constants to the
selected palette; the router then rebuilds the current view so the new colours
take effect. Pure hex only, no dependency on labforge itself (it is not
importable in the Pyodide/WASM build)."""

import flet as ft

# Palette table copied from labforge src/labforge/theme.py (pure hex, no import).
# Ordered; the first entry is the default and drives the initial render.
THEMES: dict[str, dict] = {
    "paper": {
        "note": "Warm paper surfaces, graphite ink and a vermilion accent.",
        "mode": "light",
        "accent": "#C14B2E",
        "on_accent": "#FFF6F1",
        "accent_dim": "#F2D9CE",
        "on_accent_dim": "#8A2F1B",
        "surface": "#FAF6EF",
        "surface_lowest": "#F1EAD9",
        "surface_low": "#FFFFFF",
        "surface_container": "#FFFDF8",
        "surface_high": "#FFFFFF",
        "surface_highest": "#FFFFFF",
        "on_surface": "#33302A",
        "on_surface_variant": "#7A7264",
        "outline": "#C9BFA9",
        "outline_variant": "#E5DECC",
        "model": "#2E6F8E",
    },
    "neon_gold": {
        "note": "The violet palette with pale gold as the accent instead.",
        "mode": "dark",
        "accent": "#FAEB92",
        "on_accent": "#1A0B26",
        "accent_dim": "#3E3418",
        "on_accent_dim": "#FAEB92",
        "surface": "#000000",
        "surface_lowest": "#0C0610",
        "surface_low": "#150823",
        "surface_container": "#1A0B26",
        "surface_high": "#221030",
        "surface_highest": "#29143A",
        "on_surface": "#F6EEFC",
        "on_surface_variant": "#AE90C8",
        "outline": "#43205F",
        "outline_variant": "#2B1440",
        "model": "#9929EA",
    },
    "mint": {
        "note": "Light mint greens on white, colorhunt's fresh-green family.",
        "mode": "light",
        "accent": "#3E8E5A",
        "on_accent": "#F2FBF4",
        "accent_dim": "#D8F0DC",
        "on_accent_dim": "#2C6E44",
        "surface": "#F4FAEF",
        "surface_lowest": "#E4F3DA",
        "surface_low": "#FFFFFF",
        "surface_container": "#FBFEF8",
        "surface_high": "#FFFFFF",
        "surface_highest": "#FFFFFF",
        "on_surface": "#24312A",
        "on_surface_variant": "#6D8072",
        "outline": "#B9CDB9",
        "outline_variant": "#DCE9D8",
        "model": "#B85B9E",
    },
    "lavender": {
        "note": "Soft lavender neutrals with a deep violet accent.",
        "mode": "light",
        "accent": "#7C6BD6",
        "on_accent": "#F8F6FF",
        "accent_dim": "#E3DBF7",
        "on_accent_dim": "#5A4BB0",
        "surface": "#F7F4FC",
        "surface_lowest": "#EDE6F7",
        "surface_low": "#FFFFFF",
        "surface_container": "#FCFAFF",
        "surface_high": "#FFFFFF",
        "surface_highest": "#FFFFFF",
        "on_surface": "#2C2838",
        "on_surface_variant": "#756E88",
        "outline": "#C4BBDA",
        "outline_variant": "#E4DEF1",
        "model": "#D66B8F",
    },
    # The palettes below are derived from coolors.co seeds the site owner
    # picked; surfaces/outlines are interpolated to fit the labforge schema.
    "ember": {
        "note": "Cream and ember: brick-red accent, slate-teal counterpoint.",
        "mode": "light",
        "accent": "#9E2A2B",
        "on_accent": "#FFF7E8",
        "accent_dim": "#F2D8CF",
        "on_accent_dim": "#7A1E1F",
        "surface": "#FBF3DC",
        "surface_lowest": "#F5EAC8",
        "surface_low": "#FFFFFF",
        "surface_container": "#FFFCF2",
        "surface_high": "#FFFFFF",
        "surface_highest": "#FFFFFF",
        "on_surface": "#362A28",
        "on_surface_variant": "#7E7462",
        "outline": "#D3C49B",
        "outline_variant": "#E8DFC2",
        "model": "#335C67",
    },
    "olive": {
        "note": "Olive greens on cream with a terracotta counterpoint.",
        "mode": "light",
        "accent": "#606C38",
        "on_accent": "#F9FBEA",
        "accent_dim": "#E4E6C9",
        "on_accent_dim": "#3F4A20",
        "surface": "#FEFAE0",
        "surface_lowest": "#F3EDCC",
        "surface_low": "#FFFFFF",
        "surface_container": "#FFFDF4",
        "surface_high": "#FFFFFF",
        "surface_highest": "#FFFFFF",
        "on_surface": "#283618",
        "on_surface_variant": "#6F7455",
        "outline": "#CFC9A2",
        "outline_variant": "#E7E2C4",
        "model": "#BC6C25",
    },
    "prism": {
        "note": "Black chrome with a hot-magenta accent and azure data.",
        "mode": "dark",
        "accent": "#FF006E",
        "on_accent": "#FFF0F6",
        "accent_dim": "#47001F",
        "on_accent_dim": "#FF7EB6",
        "surface": "#0D0D12",
        "surface_lowest": "#08080C",
        "surface_low": "#16161E",
        "surface_container": "#1A1A24",
        "surface_high": "#1F1F2B",
        "surface_highest": "#242432",
        "on_surface": "#F4F2F8",
        "on_surface_variant": "#A49FB4",
        "outline": "#3C3752",
        "outline_variant": "#262236",
        "model": "#3A86FF",
    },
}

DEFAULT = "paper"
# Human-facing labels for the picker (kebab keys read oddly in a dropdown).
LABELS = {
    "paper": "Paper",
    "neon_gold": "Neon Gold",
    "mint": "Mint",
    "lavender": "Lavender",
    "ember": "Ember",
    "olive": "Olive",
    "prism": "Prism",
}

# Spacing scale (theme-independent)
GUTTER = 24
SECTION_GAP = 56
MAX_CONTENT_WIDTH = 1080

# Instrument-panel accent font (bundled in assets/fonts, registered on
# page.fonts by main.py). Used for the brand, kickers, chips and dates.
FONT_MONO = "Roboto Mono"

# Active-theme state. `apply()` rebinds every constant below; views and
# components read them at build time, so a rebuild picks up the new palette.
ACTIVE_NAME = DEFAULT
MODE = "light"

ACCENT = ON_ACCENT = ACCENT_DIM = ON_ACCENT_DIM = ""
SURFACE = SURFACE_LOWEST = SURFACE_LOW = SURFACE_CONTAINER = ""
SURFACE_HIGH = SURFACE_HIGHEST = ON_SURFACE = ON_SURFACE_VARIANT = ""
OUTLINE = OUTLINE_VARIANT = HIGHLIGHT = SECONDARY = ""


def apply(name: str) -> None:
    """Rebind the module-level colour constants to the named palette.

    Unknown names fall back to the default. Call before rebuilding views."""
    global ACTIVE_NAME, MODE
    global ACCENT, ON_ACCENT, ACCENT_DIM, ON_ACCENT_DIM
    global SURFACE, SURFACE_LOWEST, SURFACE_LOW, SURFACE_CONTAINER
    global SURFACE_HIGH, SURFACE_HIGHEST, ON_SURFACE, ON_SURFACE_VARIANT
    global OUTLINE, OUTLINE_VARIANT, HIGHLIGHT, SECONDARY

    t = THEMES.get(name) or THEMES[DEFAULT]
    ACTIVE_NAME = name if name in THEMES else DEFAULT
    MODE = t["mode"]

    ACCENT = t["accent"]
    ON_ACCENT = t["on_accent"]
    ACCENT_DIM = t["accent_dim"]
    ON_ACCENT_DIM = t["on_accent_dim"]
    SURFACE = t["surface"]
    SURFACE_LOWEST = t["surface_lowest"]
    SURFACE_LOW = t["surface_low"]
    SURFACE_CONTAINER = t["surface_container"]
    SURFACE_HIGH = t["surface_high"]
    SURFACE_HIGHEST = t["surface_highest"]
    ON_SURFACE = t["on_surface"]
    ON_SURFACE_VARIANT = t["on_surface_variant"]
    OUTLINE = t["outline"]
    OUTLINE_VARIANT = t["outline_variant"]
    # Emphasis text colour: on_accent_dim is a high-contrast accent shade in both
    # light and dark modes (paper's amber highlight is too weak as text).
    HIGHLIGHT = t["on_accent_dim"]
    # Secondary accent: the palette's "model" colour.
    SECONDARY = t["model"]


def theme_mode() -> ft.ThemeMode:
    return ft.ThemeMode.DARK if MODE == "dark" else ft.ThemeMode.LIGHT


def build_theme() -> ft.Theme:
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ACCENT,
            on_primary=ON_ACCENT,
            primary_container=ACCENT_DIM,
            on_primary_container=ON_ACCENT_DIM,
            secondary=SECONDARY,
            surface=SURFACE,
            on_surface=ON_SURFACE,
            on_surface_variant=ON_SURFACE_VARIANT,
            outline=OUTLINE,
            outline_variant=OUTLINE_VARIANT,
            surface_container_highest=SURFACE_HIGHEST,
        ),
    )


# Bind the default palette at import so constants are populated before any build.
apply(DEFAULT)
