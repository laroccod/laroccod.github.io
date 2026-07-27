import flet as ft

import theme


def section_title(text: str, kicker: str = "") -> ft.Column:
    controls: list[ft.Control] = []
    if kicker:
        controls.append(
            ft.Text(kicker.upper(), size=12, color=theme.ACCENT,
                    weight=ft.FontWeight.W_600,
                    font_family=theme.FONT_MONO,
                    style=ft.TextStyle(letter_spacing=1.5))
        )
    controls.append(
        ft.Text(text, size=30, weight=ft.FontWeight.BOLD,
                color=theme.ON_SURFACE)
    )
    controls.append(
        ft.Container(width=48, height=3, bgcolor=theme.ACCENT,
                     border_radius=2, margin=ft.Margin.only(top=6))
    )
    return ft.Column(controls, spacing=4)


def content_column(controls: list, spacing: int = theme.GUTTER) -> ft.Container:
    """Centered, width-capped page body."""
    return ft.Container(
        content=ft.Column(
            controls,
            spacing=spacing,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        width=theme.MAX_CONTENT_WIDTH,
        padding=ft.Padding.symmetric(horizontal=theme.GUTTER, vertical=32),
        alignment=ft.Alignment.TOP_CENTER,
    )


def abstract_toggle(page: ft.Page, text: str,
                    label: str = "abstract") -> list[ft.Control]:
    """A "Show <label>" button plus the paragraph it reveals, as two controls
    the caller drops into a column."""
    body = ft.Container(
        content=ft.Text(text, size=13.5, color=theme.ON_SURFACE_VARIANT),
        visible=False,
        padding=ft.Padding.only(left=12, top=2, bottom=2),
        border=ft.Border(left=ft.BorderSide(2, theme.ACCENT_DIM)),
    )
    caption = ft.Text(f"Show {label}", size=13, color=theme.ACCENT)
    caret = ft.Icon(ft.Icons.EXPAND_MORE, size=18, color=theme.ACCENT)

    def toggle(e):
        body.visible = not body.visible
        caption.value = f"{'Hide' if body.visible else 'Show'} {label}"
        caret.icon = (ft.Icons.EXPAND_LESS if body.visible
                      else ft.Icons.EXPAND_MORE)
        page.update()

    button = ft.TextButton(
        content=ft.Row([caption, caret], spacing=2, tight=True),
        on_click=toggle,
    )
    # The button sits in its own Row so it hugs its content instead of
    # stretching across the card (the parent column stretches its children).
    return [ft.Row([button], spacing=0), body]


def panel(content: ft.Control, padding: int = 20) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=theme.SURFACE_CONTAINER,
        border=ft.Border.all(1, theme.OUTLINE_VARIANT),
        border_radius=12,
        padding=padding,
    )
