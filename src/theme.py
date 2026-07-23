"""Site theme: labforge's "paper" palette (warm paper surfaces, graphite ink
and a vermilion accent) — the site runs the same design system as the
framework it showcases."""

import flet as ft

# Palette values copied from labforge src/labforge/theme.py ("paper").
ACCENT = "#C14B2E"
ON_ACCENT = "#FFF6F1"
ACCENT_DIM = "#F2D9CE"
ON_ACCENT_DIM = "#8A2F1B"
SURFACE = "#FAF6EF"
SURFACE_LOWEST = "#F1EAD9"
SURFACE_LOW = "#FFFFFF"
SURFACE_CONTAINER = "#FFFDF8"
SURFACE_HIGH = "#FFFFFF"
SURFACE_HIGHEST = "#FFFFFF"
ON_SURFACE = "#33302A"
ON_SURFACE_VARIANT = "#7A7264"
OUTLINE = "#C9BFA9"
OUTLINE_VARIANT = "#E5DECC"
# Text-safe accent variant (paper's amber highlight #E0A458 is too low-contrast
# for text on light surfaces, so highlight text uses the dark rust instead).
HIGHLIGHT = "#8A2F1B"
# Secondary accent: paper's "model" color (steel blue).
SECONDARY = "#2E6F8E"

# Spacing scale
GUTTER = 24
SECTION_GAP = 56
MAX_CONTENT_WIDTH = 1080


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
