import flet as ft

import theme
from data import content


def footer() -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    f"© 2026 {content.NAME} · Built with Flet",
                    size=12,
                    color=theme.ON_SURFACE_VARIANT,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=24,
        alignment=ft.Alignment.CENTER,
    )
