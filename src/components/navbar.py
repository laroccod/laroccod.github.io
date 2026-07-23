import flet as ft

import theme
from components.wordmark import scatter_text

NAV_ITEMS = (
    ("Home", "/"),
    ("CV", "/cv"),
    ("Talks", "/presentations"),
    ("Teaching", "/teaching"),
    ("Projects", "/projects"),
    ("Contact", "/contact"),
)

# Width of the active link's underline bar; it animates from 0 on activation.
UNDERLINE_WIDTH = 20


def navbar(page: ft.Page) -> tuple[ft.Container, callable]:
    """Build the top bar.

    Returns (control, set_active). The bar persists across navigation: main.py
    calls set_active(route) on each route change, so the underline slides to
    the new link instead of the whole bar being rebuilt.
    """
    labels: dict[str, ft.Text] = {}
    underlines: dict[str, ft.Container] = {}

    def nav_link(label: str, route: str) -> ft.Control:
        text = ft.Text(label, size=14)
        bar = ft.Container(
            height=2,
            width=0,
            bgcolor=theme.ACCENT,
            border_radius=1,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        labels[route] = text
        underlines[route] = bar
        return ft.Container(
            content=ft.Column(
                [text, bar],
                spacing=3,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border_radius=6,
            ink=True,
            on_click=lambda e, r=route: page.navigate(r),
        )

    def set_active(route: str) -> None:
        if route not in labels:
            route = "/"
        for r, text in labels.items():
            active = r == route
            text.weight = ft.FontWeight.W_600 if active else ft.FontWeight.W_400
            text.color = theme.ACCENT if active else theme.ON_SURFACE_VARIANT
            underlines[r].width = UNDERLINE_WIDTH if active else 0

    # Brand mark: terminal glyph on an accent tile (labforge's app-mark style);
    # the DLR letters carry the wordmark scatter, scaled down for the top bar.
    brand_mark = ft.Container(
        width=28,
        height=28,
        border_radius=6,
        bgcolor=theme.ACCENT,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.TERMINAL, size=18, color=theme.ON_ACCENT),
    )
    brand = ft.Container(
        content=ft.Row(
            [
                brand_mark,
                scatter_text(page, "DLR", size=18, color=theme.ACCENT,
                             font_family=theme.FONT_MONO, spacing=1,
                             throw_x=0.5, throw_y=0.25, throw_rot=0.35,
                             on_click=lambda e: page.navigate("/")),
            ],
            spacing=10,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=lambda e: page.navigate("/"),
    )

    def on_theme_select(e):
        # main.py registers its theme-change handler on page.data.
        handler = page.data
        if callable(handler):
            handler(e.control.value)

    theme_picker = ft.Dropdown(
        value=theme.ACTIVE_NAME,
        options=[
            ft.DropdownOption(key=name, text=theme.LABELS[name])
            for name in theme.THEMES
        ],
        on_select=on_theme_select,
        width=150,
        text_size=13,
        dense=True,
        border_color=theme.OUTLINE,
        border_radius=8,
        bgcolor=theme.SURFACE_LOW,
        text_style=ft.TextStyle(color=theme.ON_SURFACE),
        leading_icon=ft.Icon(ft.Icons.PALETTE_OUTLINED, size=18,
                             color=theme.ON_SURFACE_VARIANT),
    )

    bar = ft.Container(
        content=ft.Row(
            [
                brand,
                ft.Row(
                    [
                        ft.Row(
                            [nav_link(label, route) for label, route in NAV_ITEMS],
                            wrap=True,
                            spacing=0,
                        ),
                        theme_picker,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.SURFACE_LOWEST,
        padding=ft.Padding.symmetric(horizontal=16, vertical=6),
        border=ft.Border(bottom=ft.BorderSide(1, theme.OUTLINE_VARIANT)),
    )
    set_active(page.route or "/")
    return bar, set_active
