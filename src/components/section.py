import flet as ft

import theme


def section_title(text: str, kicker: str = "") -> ft.Column:
    controls: list[ft.Control] = []
    if kicker:
        controls.append(
            ft.Text(kicker.upper(), size=12, color=theme.ACCENT,
                    weight=ft.FontWeight.W_600)
        )
    controls.append(
        ft.Text(text, size=30, weight=ft.FontWeight.BOLD,
                color=theme.ON_SURFACE)
    )
    controls.append(
        ft.Container(width=48, height=3, bgcolor=theme.ACCENT,
                     border_radius=2, margin=ft.Margin.only(top=6))
    )
    return ft.Column(controls, spacing=4)


def content_column(controls: list, spacing: int = theme.GUTTER) -> ft.Container:
    """Centered, width-capped page body."""
    return ft.Container(
        content=ft.Column(
            controls,
            spacing=spacing,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        width=theme.MAX_CONTENT_WIDTH,
        padding=ft.Padding.symmetric(horizontal=theme.GUTTER, vertical=32),
        alignment=ft.Alignment.TOP_CENTER,
    )


def panel(content: ft.Control, padding: int = 20) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=theme.SURFACE_CONTAINER,
        border=ft.Border.all(1, theme.OUTLINE_VARIANT),
        border_radius=12,
        padding=padding,
    )
