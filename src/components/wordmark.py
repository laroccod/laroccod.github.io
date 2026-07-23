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
              font_family: str = "", spacing: int = 0,
              autoplay_delay: float = 0.0) -> ft.Container:
    """Text as per-letter tiles that play a slow wave, then a shimmer.

    The wave rolls letter by letter: each tile rises and eases back down
    while its neighbour is still airborne, so the crest travels smoothly
    across the word. The shimmer follows: a two-letter glint of
    shimmer_color chases across the text and fades back to the base colour.

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
            # the next one lifts; the 450 ms ease outlasts the 90 ms stagger,
            # so the crest rolls without any letter pausing at the top.
            for tile in letters:
                tile.offset = ft.Offset(0, -0.42)
                page.update()
                await asyncio.sleep(0.09)
                tile.offset = ft.Offset(0, 0)
            page.update()
            await asyncio.sleep(0.45)
            # Shimmer: a two-letter glint sweeps across and restores itself.
            for i in range(len(letters) + 2):
                if i < len(letters):
                    letters[i].content.color = shimmer_color or None
                if i >= 2:
                    letters[i - 2].content.color = color or None
                page.update()
                await asyncio.sleep(0.015)
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
