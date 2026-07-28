import flet as ft

import theme
from components.chips import link_button, tech_chip
from components.section import panel
from data.projects import Project


def _lightbox(page: ft.Page, src: str, name: str, caption: str = ""):
    def open_lightbox(e):
        body: ft.Control = ft.Image(src=src, fit=ft.BoxFit.CONTAIN)
        if caption:
            body = ft.Column(
                [
                    body,
                    ft.Text(caption, size=13, color=theme.ON_SURFACE_VARIANT),
                ],
                spacing=12,
                tight=True,
            )
        page.show_dialog(
            ft.AlertDialog(
                content=body,
                bgcolor=theme.SURFACE_LOWEST,
                title=ft.Text(name, size=14, color=theme.ON_SURFACE_VARIANT),
            )
        )
    return open_lightbox


def thumb(page: ft.Page, src: str, name: str, caption: str = "",
          height: int = 150, on_light: bool = False) -> ft.Container:
    """Click-to-enlarge image tile with a hover lift.

    Paper figures and slide renders are black-on-white line art, so
    `on_light` mats them on white: on the dark palettes an unmatted plot
    reads as a floating white rectangle with no edge."""
    tile = ft.Container(
        content=ft.Image(
            src=src, height=height, fit=ft.BoxFit.CONTAIN,
            border_radius=theme.RADIUS_INNER,
        ),
        on_click=_lightbox(page, src, name, caption),
        tooltip=caption or "Click to enlarge",
        bgcolor=ft.Colors.WHITE if on_light else None,
        padding=6 if on_light else 0,
        border=ft.Border.all(1, theme.OUTLINE_VARIANT),
        border_radius=theme.RADIUS_TILE,
        scale=ft.Scale(1.0),
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )

    def on_hover(e):
        entering = str(e.data).lower() == "true"
        tile.scale = ft.Scale(1.04 if entering else 1.0)
        tile.update()

    tile.on_hover = on_hover
    return tile


def image_strip(page: ft.Page, thumbs: list[ft.Control]) -> ft.Row:
    """Row of thumbnails, sized to fit the content column on a desktop
    viewport. It wraps rather than scrolls, so a narrow viewport pushes the
    overflow onto a second line instead of hiding it behind a scrollbar."""
    return ft.Row(thumbs, wrap=True, spacing=10, run_spacing=10)


def screenshot_strip(page: ft.Page, project: Project) -> ft.Row:
    return image_strip(page, [thumb(page, src, project.name)
                              for src in project.screenshots])


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
