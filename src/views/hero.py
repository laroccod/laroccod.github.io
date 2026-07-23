import flet as ft

import theme
from components.chips import cta_button, link_button
from components.navbar import navbar
from components.footer import footer
from components.section import content_column, panel
from data import content


def build(page: ft.Page) -> ft.View:
    headshot = ft.Container(
        content=ft.Image(
            src="/headshot.jpg",
            width=260,
            height=260,
            fit=ft.BoxFit.COVER,
            border_radius=130,
        ),
        border=ft.Border.all(3, theme.ACCENT_DIM),
        border_radius=136,
        padding=4,
        width=274,
        height=274,
        alignment=ft.Alignment.CENTER,
    )

    intro = ft.Column(
        [
            ft.Text("Hi, I'm", size=18, color=theme.ON_SURFACE_VARIANT),
            ft.Text(content.NAME, size=44, weight=ft.FontWeight.BOLD,
                    color=theme.ON_SURFACE),
            ft.Text(content.TITLE, size=18, color=theme.ACCENT,
                    weight=ft.FontWeight.W_600),
            ft.Text(content.TAGLINE, size=15,
                    color=theme.ON_SURFACE_VARIANT),
            ft.Row(
                [
                    cta_button("View projects",
                               on_click=lambda e: page.navigate("/projects")),
                    cta_button("Get in touch", primary=False,
                               on_click=lambda e: page.navigate("/contact")),
                ],
                spacing=12,
                wrap=True,
            ),
        ],
        spacing=10,
    )

    hero_row = ft.ResponsiveRow(
        [
            ft.Container(intro, col={"xs": 12, "md": 7},
                         alignment=ft.Alignment.CENTER_LEFT),
            ft.Container(headshot, col={"xs": 12, "md": 5},
                         alignment=ft.Alignment.CENTER),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        run_spacing=24,
    )

    summary = panel(
        ft.Column(
            [
                ft.Text("ABOUT", size=12, color=theme.ACCENT,
                        weight=ft.FontWeight.W_600),
                ft.Text(content.SUMMARY, size=14.5, color=theme.ON_SURFACE),
            ],
            spacing=8,
        )
    )

    thesis = panel(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.SCHOOL, color=theme.PINK, size=20),
                        ft.Text("Ph.D. Thesis", size=12, color=theme.PINK,
                                weight=ft.FontWeight.W_600),
                    ],
                    spacing=8,
                ),
                ft.Text(content.THESIS_TITLE, size=17,
                        weight=ft.FontWeight.W_600, color=theme.ON_SURFACE),
                ft.Text(content.THESIS_BLURB, size=14,
                        color=theme.ON_SURFACE_VARIANT),
                ft.Row([link_button("Read on eScholarship", content.THESIS_URL,
                                    ft.Icons.MENU_BOOK)]),
            ],
            spacing=10,
        )
    )

    return ft.View(
        route="/",
        controls=[
            navbar(page),
            ft.Column(
                [content_column([hero_row, summary, thesis]), footer()],
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
