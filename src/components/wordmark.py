"""Animated wordmark, ported from labforge's top bar: the letters blow apart
when the pointer enters, float for as long as it stays, and spring back into
place the moment it leaves."""

import asyncio
import random

import flet as ft


def scatter_text(page: ft.Page, text: str, *, size: int,
                 weight: ft.FontWeight = ft.FontWeight.BOLD,
                 color: str = "", font_family: str = "",
                 spacing: int = 0, throw_x: float = 1.2, throw_y: float = 0.5,
                 throw_rot: float = 0.5, on_click=None) -> ft.Container:
    """Text rendered as per-letter tiles with the hover scatter behaviour.

    Floating is a chain of implicit animations: every beat each letter gets a
    new random target with a transition lasting exactly one beat, so a letter
    never comes to rest between targets. The float task runs via page.run_task
    so its updates reach the client; an epoch counter keeps a stale float loop
    from a previous hover writing over the current one. Throw amplitudes are
    fractions of the letter tile size.
    """
    blow = ft.Animation(500, ft.AnimationCurve.EASE_OUT_CUBIC)
    drift = ft.Animation(1200, ft.AnimationCurve.EASE_IN_OUT_SINE)
    spring = ft.Animation(400, ft.AnimationCurve.EASE_OUT_BACK)

    letters: list[ft.Container] = []
    tiles: list[ft.Control] = []
    for ch in text:
        if ch == " ":
            # Spaces are fixed spacers; only glyphs fly.
            tiles.append(ft.Container(width=size * 0.3))
            continue
        tile = ft.Container(
            content=ft.Text(ch, size=size, weight=weight,
                            color=color or None,
                            font_family=font_family or None),
            offset=ft.Offset(0, 0),
            rotate=ft.Rotate(0),
            animate_offset=spring,
            animate_rotation=spring,
        )
        letters.append(tile)
        tiles.append(tile)

    hover = {"on": False, "epoch": 0}

    def animate_with(animation: ft.Animation):
        for tile in letters:
            tile.animate_offset = animation
            tile.animate_rotation = animation

    def scatter():
        for tile in letters:
            tile.offset = ft.Offset(random.uniform(-throw_x, throw_x),
                                    random.uniform(-throw_y, throw_y))
            tile.rotate = ft.Rotate(random.uniform(-throw_rot, throw_rot))

    def settle():
        animate_with(spring)
        for tile in letters:
            tile.offset = ft.Offset(0, 0)
            tile.rotate = ft.Rotate(0)

    async def float_around(epoch: int):
        # Blow apart fast, then drift beat by beat.
        animate_with(blow)
        scatter()
        page.update()
        await asyncio.sleep(0.5)
        animate_with(drift)
        while hover["on"] and hover["epoch"] == epoch:
            scatter()
            page.update()
            await asyncio.sleep(1.2)
        # Reset only if no newer hover has taken over the letters.
        if not hover["on"]:
            settle()
            page.update()

    def on_hover(e):
        # Flet 0.86 sends hover data as a boolean: True on enter, False on exit.
        entering = str(e.data).lower() == "true"
        hover["on"] = entering
        if entering:
            hover["epoch"] += 1
            page.run_task(float_around, hover["epoch"])
        else:
            settle()
            page.update()

    return ft.Container(
        on_hover=on_hover,
        on_click=on_click,
        content=ft.Row(tiles, spacing=spacing, tight=True),
    )


def wave_text(page: ft.Page, text: str, *, size: int,
              weight: ft.FontWeight = ft.FontWeight.BOLD,
              color: str = "", shimmer_color: str = "",
              font_family: str = "", glint_font_family: str = "",
              spacing: int = 0,
              wave_seconds: float = 1.0, glint_seconds: float = 0.25,
              autoplay_delay: float = 0.0) -> ft.Container:
    """Text as per-letter tiles that play a slow wave, then a shimmer.

    The wave rolls letter by letter: each tile rises and eases back down
    while its neighbour is still airborne, so the crest travels smoothly
    across the word; it crosses the whole word in wave_seconds. The shimmer
    follows: a two-letter glint chases across the text in glint_seconds and
    restores itself. With glint_font_family set, the glint sweeps the font
    family instead of the colour: COLR color fonts (like Nabla) ignore the
    text colour, so their glint is a brighter build of the same font
    registered under a second family name.

    Plays on hover, and once on mount when autoplay_delay > 0 (seconds).
    A running flag keeps overlapping triggers from double-driving the
    letters mid-sequence.
    """
    rise = ft.Animation(450, ft.AnimationCurve.EASE_IN_OUT_SINE)

    letters: list[ft.Container] = []
    tiles: list[ft.Control] = []
    for ch in text:
        if ch == " ":
            tiles.append(ft.Container(width=size * 0.3))
            continue
        tile = ft.Container(
            content=ft.Text(ch, size=size, weight=weight,
                            color=color or None,
                            font_family=font_family or None),
            offset=ft.Offset(0, 0),
            animate_offset=rise,
        )
        letters.append(tile)
        tiles.append(tile)

    state = {"running": False}

    async def play():
        if state["running"]:
            return
        state["running"] = True
        try:
            # Slow wave: each letter starts rising, then is sent back down as
            # the next one lifts; the 450 ms ease outlasts the stagger, so
            # the crest rolls without any letter pausing at the top. The
            # stagger is derived from wave_seconds for the whole word.
            wave_step = wave_seconds / max(len(letters), 1)
            for tile in letters:
                tile.offset = ft.Offset(0, -0.42)
                page.update()
                await asyncio.sleep(wave_step)
                tile.offset = ft.Offset(0, 0)
            page.update()
            await asyncio.sleep(0.45)
            # Shimmer: a two-letter glint sweeps across and restores itself,
            # crossing the whole word in glint_seconds.
            glint_step = glint_seconds / (len(letters) + 2)
            for i in range(len(letters) + 2):
                if i < len(letters):
                    if glint_font_family:
                        letters[i].content.font_family = glint_font_family
                    else:
                        letters[i].content.color = shimmer_color or None
                if i >= 2:
                    if glint_font_family:
                        letters[i - 2].content.font_family = (font_family
                                                              or None)
                    else:
                        letters[i - 2].content.color = color or None
                page.update()
                await asyncio.sleep(glint_step)
            page.update()
        finally:
            state["running"] = False

    def on_hover(e):
        if str(e.data).lower() == "true":
            page.run_task(play)

    async def autoplay():
        await asyncio.sleep(autoplay_delay)
        await play()

    if autoplay_delay:
        page.run_task(autoplay)

    return ft.Container(
        on_hover=on_hover,
        content=ft.Row(tiles, spacing=spacing, tight=True),
    )
