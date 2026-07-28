"""Papers/Talks: publications (abstract behind a toggle, plus selected
figures) followed by conference talks and seminars (with slide previews)."""

import flet as ft

import theme
from components.cards import image_strip, thumb
from components.footer import footer
from components.section import (abstract_toggle, content_column, panel,
                                section_title)
from data import content

# Thumbnail height for the figure strips. The widest card (four figures whose
# aspect ratios sum to ~6.2) then measures ~930 px, inside the ~996 px of
# content column the panel leaves, so the row fits without scrolling.
# Every card uses it, single-figure ones included: a taller thumbnail there
# fits the row fine but reads as a banner next to the plot strips.
FIGURE_HEIGHT = 135


def _strip_caption(lead: str, single: bool = False) -> ft.Text:
    tail = "Click to enlarge." if single else "Click one to enlarge."
    return ft.Text(f"{lead} {tail}", size=12, italic=True,
                   color=theme.ON_SURFACE_VARIANT)


def _publication(page: ft.Page, pub: content.Publication) -> ft.Container:
    rows: list[ft.Control] = [
        ft.Text(pub.title, size=17, weight=ft.FontWeight.W_600,
                color=theme.ON_SURFACE),
        ft.Text(pub.authors, size=13, color=theme.ON_SURFACE_VARIANT),
        ft.Row(
            [
                ft.Text(f"{pub.venue} ({pub.year})", size=13,
                        color=theme.ACCENT, expand=True),
                ft.TextButton(content=ft.Text("View ↗", size=13), url=pub.url),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    ]
    if pub.abstract:
        rows.extend(abstract_toggle(page, pub.abstract))
    if pub.figures:
        solo = len(pub.figures) == 1
        rows.append(
            image_strip(page, [
                thumb(page, f.src, pub.title, caption=f.caption,
                      height=FIGURE_HEIGHT, on_light=True)
                for f in pub.figures
            ])
        )
        rows.append(_strip_caption(
            "Select figure." if solo else "Select figures.", single=solo))
    return panel(ft.Column(rows, spacing=8), padding=18)


def _talk(page: ft.Page, p: content.Presentation) -> ft.Container:
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
    if p.previews:
        rows.append(
            image_strip(page, [
                thumb(page, src, p.event, height=130, on_light=True)
                for src in p.previews
            ])
        )
        rows.append(_strip_caption("Select slides."))
    return panel(ft.Column(rows, spacing=6), padding=16)


def build(page: ft.Page) -> ft.Control:
    body = content_column(
        [
            section_title("Publications", kicker="Papers/Talks"),
            ft.Text(
                "Peer-reviewed work on heavy neutral leptons and the "
                "simulation tools behind it, plus earlier computational "
                "biophysics from my undergraduate research.",
                size=14.5, color=theme.ON_SURFACE_VARIANT,
            ),
            *[_publication(page, p) for p in content.PUBLICATIONS],
            section_title("Conference Talks & Seminars"),
            ft.Text(
                "International conference presentations, invited seminars, "
                "and my Ph.D. thesis defense, 2024–2026.",
                size=14.5, color=theme.ON_SURFACE_VARIANT,
            ),
            *[_talk(page, p) for p in content.PRESENTATIONS],
        ]
    )

    return ft.Column(
        [body, footer()],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
