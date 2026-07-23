import flet as ft

import theme
from components.navbar import navbar
from components.footer import footer
from components.section import content_column, panel, section_title
from data import content


def _talk(p: content.Presentation) -> ft.Container:
    rows: list[ft.Control] = [
        ft.Row(
            [
                ft.Text(p.date, size=13, color=theme.ACCENT,
                        weight=ft.FontWeight.W_600),
                ft.Container(
                    content=ft.Text(p.kind, size=11,
                                    color=theme.ON_ACCENT_DIM),
                    bgcolor=theme.ACCENT_DIM,
                    border_radius=999,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                ),
            ],
            spacing=10,
            wrap=True,
        ),
        ft.Text(p.title, size=15, weight=ft.FontWeight.W_600,
                color=theme.ON_SURFACE),
        ft.Text(f"{p.event} · {p.where}", size=13,
                color=theme.ON_SURFACE_VARIANT),
    ]
    links: list[ft.Control] = []
    if p.url:
        links.append(
            ft.TextButton(content=ft.Text("Event page ↗", size=13), url=p.url)
        )
    if p.slides:
        links.append(
            ft.TextButton(content=ft.Text("Slides (PDF) ↗", size=13),
                          url=p.slides)
        )
    if links:
        rows.append(ft.Row(links, spacing=4, wrap=True))
    return panel(ft.Column(rows, spacing=6), padding=16)


def build(page: ft.Page) -> ft.View:
    body = content_column(
        [
            section_title("Conference Talks & Seminars", kicker="Presentations"),
            ft.Text(
                "International conference presentations, invited seminars, "
                "and my Ph.D. thesis defense, 2024–2026.",
                size=14.5, color=theme.ON_SURFACE_VARIANT,
            ),
            *[_talk(p) for p in content.PRESENTATIONS],
        ]
    )

    return ft.View(
        route="/presentations",
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
