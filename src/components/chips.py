import flet as ft

import theme


def tech_chip(label: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(label, size=12, color=theme.ON_ACCENT_DIM),
        bgcolor=theme.ACCENT_DIM,
        border_radius=999,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
    )


def link_button(label: str, url: str, icon=None) -> ft.OutlinedButton:
    """External-link button; renders nothing useful if url is empty — callers
    should skip empty urls."""
    return ft.OutlinedButton(
        content=ft.Row(
            [
                ft.Icon(icon or ft.Icons.OPEN_IN_NEW, size=16),
                ft.Text(label),
            ],
            spacing=6,
            tight=True,
        ),
        url=url,
    )


def cta_button(label: str, on_click=None, url: str = "", primary=True):
    kwargs = {"url": url} if url else {"on_click": on_click}
    if primary:
        return ft.FilledButton(
            content=ft.Text(label, weight=ft.FontWeight.W_600,
                            color=theme.ON_ACCENT),
            bgcolor=theme.ACCENT,
            **kwargs,
        )
    return ft.OutlinedButton(
        content=ft.Text(label, weight=ft.FontWeight.W_600,
                        color=theme.ACCENT),
        **kwargs,
    )
