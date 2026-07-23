import asyncio

import flet as ft

import theme
from components.chips import cta_button, link_button
from components.footer import footer
from components.section import content_column, panel
from components.wordmark import wave_text
from data import content


def build(page: ft.Page) -> ft.Control:
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
            # Name plays a slow wave then an accent shimmer: once on load
            # (right after the entrance reveal) and again on hover.
            wave_text(page, content.NAME, size=44,
                      color=theme.ON_SURFACE, shimmer_color=theme.ACCENT,
                      autoplay_delay=0.7),
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

    # Entrance: the hero row fades in and rises a touch on mount.
    reveal = ft.Container(
        content=hero_row,
        opacity=0,
        offset=ft.Offset(0, 0.04),
        animate_opacity=ft.Animation(450, ft.AnimationCurve.EASE_OUT),
        animate_offset=ft.Animation(450, ft.AnimationCurve.EASE_OUT),
    )

    async def enter():
        # One beat for the frame to mount, then animate to the final values.
        await asyncio.sleep(0.06)
        reveal.opacity = 1
        reveal.offset = ft.Offset(0, 0)
        page.update()

    page.run_task(enter)

    summary = panel(
        ft.Column(
            [
                ft.Text("ABOUT", size=12, color=theme.ACCENT,
                        weight=ft.FontWeight.W_600,
                        font_family=theme.FONT_MONO,
                        style=ft.TextStyle(letter_spacing=1.5)),
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
                        ft.Icon(ft.Icons.SCHOOL, color=theme.SECONDARY, size=20),
                        ft.Text("PH.D. THESIS", size=12, color=theme.SECONDARY,
                                weight=ft.FontWeight.W_600,
                                font_family=theme.FONT_MONO,
                                style=ft.TextStyle(letter_spacing=1.5)),
                    ],
                    spacing=8,
                ),
                ft.Text(content.THESIS_TITLE, size=17,
                        weight=ft.FontWeight.W_600, color=theme.ON_SURFACE),
                ft.Text(content.THESIS_BLURB, size=14,
                        color=theme.ON_SURFACE_VARIANT),
                ft.Row(
                    [
                        link_button("Read on eScholarship", content.THESIS_URL,
                                    ft.Icons.MENU_BOOK),
                        link_button("Defense slides (PDF)",
                                    content.DEFENSE_SLIDES,
                                    ft.Icons.PICTURE_AS_PDF),
                    ],
                    wrap=True,
                    spacing=8,
                    run_spacing=8,
                ),
            ],
            spacing=10,
        )
    )

    return ft.Column(
        [content_column([reveal, summary, thesis]), footer()],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
