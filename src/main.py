import asyncio

import flet as ft

import theme
from components.navbar import navbar
from data import content
from views import contact, cv, hero, presentations, projects, teaching

ROUTES = {
    "/": hero.build,
    "/cv": cv.build,
    "/presentations": presentations.build,
    "/teaching": teaching.build,
    "/projects": projects.build,
    "/contact": contact.build,
}

# client-storage key for the visitor's chosen theme
THEME_PREF_KEY = "portfolio.theme"

# Navigation fade-in (ms): quick enough to read as a soft cut, not a wipe.
# (ft.AnimatedSwitcher renders blank on the 0.86 web runtime, so the fade is
# done by hand: swap the pane's content at opacity 0, then animate to 1.)
NAV_FADE_MS = 90


async def main(page: ft.Page):
    page.title = f"{content.NAME} · Particle Physics & Scientific Software"
    page.padding = 0
    page.fonts = {theme.FONT_MONO: "/fonts/RobotoMono.ttf"}

    prefs = ft.SharedPreferences()

    # The persistent chrome. build_shell() fills these; navigation reuses them,
    # so a route change only swaps the pane's content (with a fade) and slides
    # the navbar underline instead of rebuilding the whole page.
    shell = {"pane": None, "set_active": None}

    def configure_page():
        """Push the active palette onto the page (theme, mode, background)."""
        page.theme = theme.build_theme()
        page.dark_theme = theme.build_theme()
        page.theme_mode = theme.theme_mode()
        page.bgcolor = theme.SURFACE

    async def fade_in():
        # One beat at opacity 0 so the swap lands, then animate to full.
        await asyncio.sleep(0.05)
        shell["pane"].opacity = 1
        page.update()

    def show_route(fade: bool = True):
        pane = shell["pane"]
        pane.content = ROUTES.get(page.route, hero.build)(page)
        shell["set_active"](page.route)
        if fade:
            pane.opacity = 0
            page.update()
            page.run_task(fade_in)
        else:
            pane.opacity = 1
            page.update()

    def build_shell():
        """(Re)build the persistent chrome: navbar + fading body pane.

        Called at startup and on theme change (views read the colour constants
        at build time, so a palette switch needs a full rebuild)."""
        bar, set_active = navbar(page)
        shell["set_active"] = set_active
        shell["pane"] = ft.Container(
            expand=True,
            content=ROUTES.get(page.route, hero.build)(page),
            animate_opacity=ft.Animation(NAV_FADE_MS, ft.AnimationCurve.EASE_OUT),
        )
        page.views.clear()
        page.views.append(
            ft.View(
                route=page.route,
                controls=[bar, shell["pane"]],
                padding=0,
                spacing=0,
                bgcolor=theme.SURFACE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def route_change():
        show_route()

    def change_theme(name: str):
        """Navbar theme-picker handler (registered on page.data)."""
        theme.apply(name)
        configure_page()
        build_shell()
        page.update()
        # Persist in the background; failure must never break switching.
        page.run_task(prefs.set, THEME_PREF_KEY, name)

    page.data = change_theme
    page.on_route_change = route_change

    # Restore a previously chosen theme (best-effort; defaults to paper).
    try:
        saved = await prefs.get(THEME_PREF_KEY)
        if isinstance(saved, str) and saved in theme.THEMES:
            theme.apply(saved)
    except Exception:
        pass

    configure_page()
    build_shell()
    page.update()


ft.run(main)
