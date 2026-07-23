import flet as ft

import theme
from components.cards import timeline_entry
from components.chips import tech_chip
from components.navbar import navbar
from components.footer import footer
from components.section import content_column, panel, section_title
from data import content


def build(page: ft.Page) -> ft.View:
    skills = panel(
        ft.Column(
            [
                ft.Column(
                    [
                        ft.Text(group.name, size=14, weight=ft.FontWeight.W_600,
                                color=theme.HIGHLIGHT),
                        ft.Row([tech_chip(i) for i in group.items], wrap=True,
                               spacing=6, run_spacing=6),
                    ],
                    spacing=6,
                )
                for group in content.SKILLS
            ],
            spacing=16,
        )
    )

    experience = [
        timeline_entry(e.role, f"{e.org} · {e.advisor}", e.dates,
                       bullets=e.bullets)
        for e in content.EXPERIENCE
    ]

    education = [
        timeline_entry(e.school, e.degree, e.dates, details=e.details)
        for e in content.EDUCATION
    ]

    publications = [
        panel(
            ft.Column(
                [
                    ft.Text(p.title, size=15, weight=ft.FontWeight.W_600,
                            color=theme.ON_SURFACE),
                    ft.Text(p.authors, size=13,
                            color=theme.ON_SURFACE_VARIANT),
                    ft.Row(
                        [
                            ft.Text(f"{p.venue} ({p.year})", size=13,
                                    color=theme.ACCENT, expand=True),
                            ft.TextButton(
                                content=ft.Text("View ↗", size=13),
                                url=p.url,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=6,
            ),
            padding=16,
        )
        for p in content.PUBLICATIONS
    ]

    teaching = panel(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("▸", color=theme.ACCENT, size=13),
                        ft.Text(t, size=13.5, color=theme.ON_SURFACE,
                                expand=True),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=8,
                )
                for t in content.TEACHING
            ],
            spacing=8,
        )
    )

    body = content_column(
        [
            section_title("Curriculum Vitae", kicker="CV"),
            ft.Text(content.SUMMARY, size=14.5,
                    color=theme.ON_SURFACE_VARIANT),
            section_title("Research Experience"),
            *experience,
            section_title("Education"),
            *education,
            section_title("Technical Skills"),
            skills,
            section_title("Publications"),
            *publications,
            section_title("Teaching, Service & Outreach"),
            teaching,
        ]
    )

    return ft.View(
        route="/cv",
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
