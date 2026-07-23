import flet as ft

import theme

NAV_ITEMS = (
    ("Home", "/"),
    ("CV", "/cv"),
    ("Talks", "/presentations"),
    ("Projects", "/projects"),
    ("Contact", "/contact"),
)


def navbar(page: ft.Page) -> ft.Container:
    def nav_link(label: str, route: str) -> ft.Control:
        active = page.route == route or (route == "/" and page.route in ("", None))
        return ft.TextButton(
            content=ft.Text(
                label,
                weight=ft.FontWeight.W_600 if active else ft.FontWeight.W_400,
                color=theme.ACCENT if active else theme.ON_SURFACE_VARIANT,
            ),
            on_click=lambda e, r=route: page.navigate(r),
        )

    brand = ft.TextButton(
        content=ft.Text("DLR", size=18, weight=ft.FontWeight.BOLD,
                        color=theme.ACCENT),
        on_click=lambda e: page.navigate("/"),
    )

    return ft.Container(
        content=ft.Row(
            [
                brand,
                ft.Row(
                    [nav_link(label, route) for label, route in NAV_ITEMS],
                    wrap=True,
                    spacing=0,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=True,
        ),
        bgcolor=theme.SURFACE_LOWEST,
        padding=ft.Padding.symmetric(horizontal=16, vertical=6),
        border=ft.Border(bottom=ft.BorderSide(1, theme.OUTLINE_VARIANT)),
    )
