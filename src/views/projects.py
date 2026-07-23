import flet as ft

import theme
from components.cards import project_card
from components.navbar import navbar
from components.footer import footer
from components.section import content_column, section_title
from data.projects import PROJECTS


def build(page: ft.Page) -> ft.View:
    featured = [p for p in PROJECTS if p.featured]
    other = [p for p in PROJECTS if not p.featured]

    other_grid = ft.ResponsiveRow(
        [
            ft.Container(project_card(page, p), col={"xs": 12, "lg": 6})
            for p in other
        ],
        run_spacing=theme.GUTTER,
        spacing=theme.GUTTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    body = content_column(
        [
            section_title("Projects", kicker="Software"),
            ft.Text(
                "Interactive scientific applications and the open-source "
                "research software behind my publications. Live demos are "
                "wired in as they come online; screenshots and source links "
                "in the meantime.",
                size=14.5, color=theme.ON_SURFACE_VARIANT,
            ),
            *[project_card(page, p) for p in featured],
            section_title("Research software"),
            other_grid,
        ]
    )

    return ft.View(
        route="/projects",
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
