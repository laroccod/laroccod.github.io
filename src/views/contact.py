import flet as ft

import theme
from components.navbar import navbar
from components.footer import footer
from components.section import content_column, panel, section_title
from data import content

_ICONS = {
    "EMAIL": ft.Icons.EMAIL,
    "CODE": ft.Icons.CODE,
    "SCHOOL": ft.Icons.SCHOOL,
    "WORK": ft.Icons.WORK,
    "BADGE": ft.Icons.BADGE,
}


def build(page: ft.Page) -> ft.View:
    links = [
        panel(
            ft.Row(
                [
                    ft.Icon(_ICONS.get(link.icon, ft.Icons.OPEN_IN_NEW),
                            color=theme.ACCENT),
                    ft.Column(
                        [
                            ft.Text(link.label, size=15,
                                    weight=ft.FontWeight.W_600,
                                    color=theme.ON_SURFACE),
                            ft.Text(
                                link.url.removeprefix("mailto:"),
                                size=13, color=theme.ON_SURFACE_VARIANT),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.IconButton(icon=ft.Icons.OPEN_IN_NEW, url=link.url,
                                  icon_color=theme.ON_SURFACE_VARIANT),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=16,
        )
        for link in content.CONTACT_LINKS
    ]

    body = content_column(
        [
            section_title("Get in Touch", kicker="Contact"),
            ft.Text(
                f"Based in {content.LOCATION}. The fastest way to reach me "
                "is email. I'm happy to talk about research software, "
                "simulation tooling, and opportunities.",
                size=14.5, color=theme.ON_SURFACE_VARIANT,
            ),
            *links,
        ]
    )

    return ft.View(
        route="/contact",
        controls=[
            navbar(page),
            ft.Column(
                [body, footer()],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
        ],
        padding=0,
        spacing=0,
        bgcolor=theme.SURFACE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
