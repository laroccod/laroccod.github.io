import flet as ft

import theme
from components.chips import link_button, tech_chip
from components.section import panel
from data.projects import Project


def _lightbox(page: ft.Page, src: str, name: str):
    def open_lightbox(e):
        page.show_dialog(
            ft.AlertDialog(
                content=ft.Image(src=src, fit=ft.BoxFit.CONTAIN),
                bgcolor=theme.SURFACE_LOWEST,
                title=ft.Text(name, size=14, color=theme.ON_SURFACE_VARIANT),
            )
        )
    return open_lightbox


def _thumb(page: ft.Page, src: str, name: str) -> ft.Container:
    tile = ft.Container(
        content=ft.Image(
            src=src, height=150, fit=ft.BoxFit.CONTAIN, border_radius=8,
        ),
        on_click=_lightbox(page, src, name),
        tooltip="Click to enlarge",
        border=ft.Border.all(1, theme.OUTLINE_VARIANT),
        border_radius=8,
        scale=ft.Scale(1.0),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )

    def on_hover(e):
        entering = str(e.data).lower() == "true"
        tile.scale = ft.Scale(1.04 if entering else 1.0)
        tile.update()

    tile.on_hover = on_hover
    return tile


def screenshot_strip(page: ft.Page, project: Project) -> ft.Row:
    thumbs = [_thumb(page, src, project.name) for src in project.screenshots]
    return ft.Row(thumbs, scroll=ft.ScrollMode.AUTO, spacing=10)


def project_card(page: ft.Page, project: Project) -> ft.Container:
    links: list[ft.Control] = []
    if project.github_url:
        links.append(link_button("GitHub", project.github_url, ft.Icons.CODE))
    if project.pypi_url:
        links.append(link_button("PyPI", project.pypi_url, ft.Icons.INVENTORY_2))
    if project.demo_url:
        links.append(link_button("Launch live demo", project.demo_url,
                                 ft.Icons.ROCKET_LAUNCH))
    if project.docs_url:
        links.append(link_button("Docs", project.docs_url, ft.Icons.DESCRIPTION))
    if not project.github_url and project.slug == "foresee-lab":
        links.append(ft.Text("Public release coming soon", size=12,
                             italic=True, color=theme.ON_SURFACE_VARIANT))

    header = ft.Row(
        [
            ft.Text(project.name, size=22, weight=ft.FontWeight.BOLD,
                    color=theme.ON_SURFACE),
            ft.Text(project.role, size=12, color=theme.SECONDARY,
                    weight=ft.FontWeight.W_600),
        ],
        spacing=14,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    body: list[ft.Control] = [
        header,
        ft.Text(project.tagline, size=14, color=theme.HIGHLIGHT, italic=True),
        ft.Text(project.description, size=14, color=theme.ON_SURFACE_VARIANT),
        ft.Row([tech_chip(t) for t in project.tech], wrap=True, spacing=6,
               run_spacing=6),
    ]
    if project.screenshots:
        body.append(screenshot_strip(page, project))
    if links:
        body.append(ft.Row(links, wrap=True, spacing=8, run_spacing=8))

    return panel(ft.Column(body, spacing=14))


def timeline_entry(title: str, subtitle: str, dates: str,
                   bullets: tuple[str, ...] = (),
                   details: tuple[str, ...] = ()) -> ft.Container:
    rows: list[ft.Control] = [
        ft.Row(
            [
                ft.Text(title, size=17, weight=ft.FontWeight.W_600,
                        color=theme.ON_SURFACE, expand=True),
                ft.Text(dates, size=13, color=theme.ACCENT,
                        font_family=theme.FONT_MONO),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        ft.Text(subtitle, size=14, color=theme.ON_SURFACE_VARIANT),
    ]
    for d in details:
        rows.append(ft.Text(d, size=13, color=theme.ON_SURFACE_VARIANT))
    for b in bullets:
        rows.append(
            ft.Row(
                [
                    ft.Text("▸", color=theme.ACCENT, size=13),
                    ft.Text(b, size=13.5, color=theme.ON_SURFACE, expand=True),
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=8,
            )
        )
    return panel(ft.Column(rows, spacing=8))
