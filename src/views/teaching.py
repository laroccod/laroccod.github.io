import flet as ft

import theme
from components.cards import timeline_entry
from components.chips import tech_chip
from components.footer import footer
from components.section import content_column, panel, section_title
from data import content


def build(page: ft.Page) -> ft.Control:
    roles = [
        timeline_entry(r.role, r.org, r.dates, bullets=r.bullets)
        for r in content.TEACHING_ROLES
    ]

    courses = panel(
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
                for group in content.COURSES_PREPARED
            ],
            spacing=16,
        )
    )

    mentoring = panel(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("▸", color=theme.ACCENT, size=13),
                        ft.Text(m, size=13.5, color=theme.ON_SURFACE,
                                expand=True),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=8,
                )
                for m in content.MENTORING
            ],
            spacing=8,
        )
    )

    body = content_column(
        [
            section_title("Teaching Experience", kicker="Teaching"),
            ft.Text(content.TEACHING_PROFILE, size=14.5,
                    color=theme.ON_SURFACE_VARIANT),
            *roles,
            section_title("Courses Prepared to Teach"),
            courses,
            section_title("Mentoring & Outreach"),
            mentoring,
        ]
    )

    return ft.Column(
        [body, footer()],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
