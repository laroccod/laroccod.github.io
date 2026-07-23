import flet as ft

import theme
from components.wordmark import scatter_text

NAV_ITEMS = (
    ("Home", "/"),
    ("CV", "/cv"),
    ("Talks", "/presentations"),
    ("Teaching", "/teaching"),
    ("Projects", "/projects"),
    ("Contact", "/contact"),
)
VALID_ROUTES = {route for _, route in NAV_ITEMS}

# Width of the active link's underline bar; it animates from 0 on activation.
UNDERLINE_WIDTH = 20

# At or below this page width the horizontal links + theme picker no longer fit,
# so the bar collapses to a brand + hamburger row with a drop-down menu.
MOBILE_MAX_WIDTH = 780


def navbar(page: ft.Page) -> tuple[ft.Container, callable]:
    """Build the top bar.

    Returns (control, set_active). The bar persists across navigation: main.py
    calls set_active(route) on each route change, so the underline slides to
    the new link instead of the whole bar being rebuilt.

    The bar is responsive: on wide viewports it shows the full horizontal link
    row and theme picker; at/below MOBILE_MAX_WIDTH it collapses to a hamburger
    that toggles a stacked drop-down menu (page.on_resize flips between the two).
    """
    # Each link (desktop and mobile) registers a closure that restyles it for a
    # given active route; set_active just fans out to all of them.
    updaters: list[callable] = []

    def desktop_link(label: str, route: str) -> ft.Control:
        text = ft.Text(label, size=14)
        bar = ft.Container(
            height=2,
            width=0,
            bgcolor=theme.ACCENT,
            border_radius=1,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )

        def update(active: str) -> None:
            on = active == route
            text.weight = ft.FontWeight.W_600 if on else ft.FontWeight.W_400
            text.color = theme.ACCENT if on else theme.ON_SURFACE_VARIANT
            bar.width = UNDERLINE_WIDTH if on else 0

        updaters.append(update)
        return ft.Container(
            content=ft.Column(
                [text, bar],
                spacing=3,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border_radius=6,
            ink=True,
            on_click=lambda e, r=route: page.navigate(r),
        )

    def mobile_link(label: str, route: str) -> ft.Control:
        text = ft.Text(label, size=16)
        row = ft.Container(
            content=text,
            padding=ft.Padding.symmetric(horizontal=14, vertical=13),
            border_radius=8,
            ink=True,
            on_click=lambda e, r=route: (set_menu(False), page.navigate(r)),
        )

        def update(active: str) -> None:
            on = active == route
            text.weight = ft.FontWeight.W_600 if on else ft.FontWeight.W_400
            text.color = theme.HIGHLIGHT if on else theme.ON_SURFACE
            row.bgcolor = theme.ACCENT_DIM if on else None

        updaters.append(update)
        return row

    def set_active(route: str) -> None:
        if route not in VALID_ROUTES:
            route = "/"
        for update in updaters:
            update(route)

    # Brand mark: terminal glyph on an accent tile (labforge's app-mark style);
    # the DLR letters carry the wordmark scatter, scaled down for the top bar.
    brand_mark = ft.Container(
        width=28,
        height=28,
        border_radius=6,
        bgcolor=theme.ACCENT,
        alignment=ft.Alignment.CENTER,
        content=ft.Icon(ft.Icons.TERMINAL, size=18, color=theme.ON_ACCENT),
    )
    brand = ft.Container(
        content=ft.Row(
            [
                brand_mark,
                scatter_text(page, "DLR", size=18, color=theme.ACCENT,
                             font_family=theme.FONT_MONO, spacing=1,
                             throw_x=0.5, throw_y=0.25, throw_rot=0.35,
                             on_click=lambda e: page.navigate("/")),
            ],
            spacing=10,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        on_click=lambda e: page.navigate("/"),
    )

    def on_theme_select(e):
        # main.py registers its theme-change handler on page.data.
        handler = page.data
        if callable(handler):
            handler(e.control.value)

    def make_theme_picker(width) -> ft.Dropdown:
        return ft.Dropdown(
            value=theme.ACTIVE_NAME,
            options=[
                ft.DropdownOption(key=name, text=theme.LABELS[name])
                for name in theme.THEMES
            ],
            on_select=on_theme_select,
            width=width,
            text_size=13,
            dense=True,
            border_color=theme.OUTLINE,
            border_radius=8,
            bgcolor=theme.SURFACE_LOW,
            text_style=ft.TextStyle(color=theme.ON_SURFACE),
            leading_icon=ft.Icon(ft.Icons.PALETTE_OUTLINED, size=18,
                                 color=theme.ON_SURFACE_VARIANT),
        )

    # --- Desktop cluster: horizontal links + theme picker (hidden on mobile) ---
    desktop_cluster = ft.Row(
        [
            ft.Row(
                [desktop_link(label, route) for label, route in NAV_ITEMS],
                spacing=0,
            ),
            make_theme_picker(150),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    # --- Mobile: hamburger toggle + stacked drop-down menu ------------------
    menu_open = {"v": False}

    hamburger = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_color=theme.ON_SURFACE,
        icon_size=24,
        on_click=lambda e: set_menu(not menu_open["v"]),
        visible=False,
    )

    mobile_menu = ft.Container(
        visible=False,
        padding=ft.Padding.only(left=6, right=6, top=6, bottom=10),
        content=ft.Column(
            [
                *[mobile_link(label, route) for label, route in NAV_ITEMS],
                ft.Container(
                    content=ft.Divider(height=1, color=theme.OUTLINE_VARIANT),
                    padding=ft.Padding.symmetric(vertical=8, horizontal=8),
                ),
                ft.Container(
                    content=make_theme_picker(None),
                    padding=ft.Padding.symmetric(horizontal=8),
                ),
            ],
            spacing=2,
            tight=True,
        ),
    )

    def set_menu(open_: bool) -> None:
        menu_open["v"] = open_
        mobile_menu.visible = open_
        hamburger.icon = ft.Icons.CLOSE if open_ else ft.Icons.MENU
        page.update()

    def relayout(width: float | None = None) -> None:
        """Point the bar at the layout the given width can fit.

        Called at build time (width falls back to page.width, no page.update)
        and from page.on_resize (which passes the event's fresh width, since
        page.width is not yet updated when the handler runs)."""
        w = width if width is not None else page.width
        mobile = (w or 1200) <= MOBILE_MAX_WIDTH
        hamburger.visible = mobile
        desktop_cluster.visible = not mobile
        if not mobile:
            menu_open["v"] = False
            hamburger.icon = ft.Icons.MENU
        mobile_menu.visible = mobile and menu_open["v"]

    def on_resize(e) -> None:
        # The event carries the fresh width; page.width lags one frame here.
        relayout(getattr(e, "width", None))
        page.update()

    page.on_resize = on_resize

    top_row = ft.Row(
        [brand, desktop_cluster, hamburger],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    bar = ft.Container(
        content=ft.Column([top_row, mobile_menu], spacing=0, tight=True),
        bgcolor=theme.SURFACE_LOWEST,
        padding=ft.Padding.symmetric(horizontal=16, vertical=6),
        border=ft.Border(bottom=ft.BorderSide(1, theme.OUTLINE_VARIANT)),
    )
    relayout()
    set_active(page.route or "/")
    return bar, set_active
