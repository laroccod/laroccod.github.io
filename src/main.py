import flet as ft

import theme
from data import content
from views import contact, cv, hero, presentations, projects

ROUTES = {
    "/": hero.build,
    "/cv": cv.build,
    "/presentations": presentations.build,
    "/projects": projects.build,
    "/contact": contact.build,
}


def main(page: ft.Page):
    page.title = f"{content.NAME} — Particle Physics & Scientific Software"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = theme.build_theme()
    page.dark_theme = theme.build_theme()
    page.bgcolor = theme.SURFACE
    page.padding = 0

    def route_change():
        builder = ROUTES.get(page.route, hero.build)
        page.views.clear()
        page.views.append(builder(page))
        page.update()

    page.on_route_change = route_change
    route_change()


ft.run(main)
