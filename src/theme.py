"""Site theme: labforge's "instrument" palette (near-black teal surfaces,
one electric accent) — the site runs the same design system as the framework
it showcases."""

import flet as ft

# Palette values copied from labforge src/labforge/theme.py ("instrument").
ACCENT = "#2BE4C8"
ON_ACCENT = "#04211C"
ACCENT_DIM = "#123B33"
ON_ACCENT_DIM = "#7FEFD9"
SURFACE = "#0B0F10"
SURFACE_LOWEST = "#080C0D"
SURFACE_LOW = "#11181A"
SURFACE_CONTAINER = "#141C1E"
SURFACE_HIGH = "#182123"
SURFACE_HIGHEST = "#1C2628"
ON_SURFACE = "#E4EBEA"
ON_SURFACE_VARIANT = "#8CA0A0"
OUTLINE = "#3C4C4E"
OUTLINE_VARIANT = "#233032"
HIGHLIGHT = "#7FEFD9"
PINK = "#FF4D9E"

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
            secondary=PINK,
            surface=SURFACE,
            on_surface=ON_SURFACE,
            on_surface_variant=ON_SURFACE_VARIANT,
            outline=OUTLINE,
            outline_variant=OUTLINE_VARIANT,
            surface_container_highest=SURFACE_HIGHEST,
        ),
    )
