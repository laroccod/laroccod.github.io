"""Matrix-style glyph rain, tuned for the Pyodide web build.

Columns of physics symbols (Greek letters, operators, digits) fall behind the
hero headshot. Python never drives frames: each drop is a Container whose
``offset`` is tweened by Flutter's implicit animation, so a Python task only
wakes to retarget a drop once per fall (a couple of ``page.update()`` calls per
second in total), the same trick as the wordmark animations.

Lifecycle: the router swaps the body pane on navigation but asyncio tasks keep
running, so each loop checks (a) a per-page epoch that a newer build bumps
(theme switches rebuild the hero on the same route) and (b) that the page is
still on the route the rain was built for, and exits otherwise.
"""

import asyncio
import random

import flet as ft

import theme

# RobotoMono-covered physics set (checked against the bundled TTF's cmap;
# hbar U+210F is missing from the font, so it stays out).
GLYPHS = "ψνμπλφητρσξδεθΣΔΩΛΦΨ∂∫≈∞√±0123456789"

FALL_MS = (6000, 13000)  # per-drop fall duration range
TRAIL = (5, 8)           # glyphs per drop
SNAP = ft.Animation(1, ft.AnimationCurve.LINEAR)  # ~instant jump back to top

def matrix_rain(page: ft.Page, *, width: int = 340, height: int = 340,
                columns: int = 10, font_size: int = 13) -> ft.Container:
    """A clipped panel of falling glyph columns sized width x height."""
    # Per-page epoch: a newer build on the same page (theme switch, revisit)
    # invalidates this build's loops. Kept on the page, not module-global,
    # because `flet run` serves every browser session from one process and a
    # global would let one session's build kill another session's rain.
    epoch = getattr(page, "_rain_epoch", 0) + 1
    page._rain_epoch = epoch
    home_route = page.route

    def alive() -> bool:
        return getattr(page, "_rain_epoch", 0) == epoch \
            and page.route == home_route

    col_w = width / columns
    line_h = font_size * 1.4  # estimate; offsets are in units of drop height

    drops: list[tuple[ft.Container, list[ft.Text], float]] = []
    for i in range(columns):
        trail = random.randint(*TRAIL)
        # Most columns rain in the accent; roughly one in four in the
        # secondary (model) colour for a little depth.
        base = theme.SECONDARY if random.random() < 0.25 else theme.ACCENT
        texts = []
        for j in range(trail):
            # Tail (top) fades out, head (bottom) is brightest.
            alpha = 0.10 + 0.80 * (j / (trail - 1))
            texts.append(ft.Text(random.choice(GLYPHS), size=font_size,
                                 font_family=theme.FONT_MONO,
                                 color=ft.Colors.with_opacity(alpha, base)))
        drop_h = trail * line_h
        travel = height / drop_h + 0.15  # offset units: fully past the bottom
        drop = ft.Container(
            content=ft.Column(texts, spacing=0, tight=True,
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            left=i * col_w + (col_w - font_size) / 2,
            top=0,
            offset=ft.Offset(0, -1.05),  # start hidden above the field
            animate_offset=SNAP,
        )
        drops.append((drop, texts, travel))

    async def run_drop(drop: ft.Container, texts: list[ft.Text],
                       travel: float):
        # Seed the first cycle mid-flight: without this every drop starts
        # above the field at once and the first wave falls as one clump with
        # a long empty gap behind it. A random head start spreads the columns
        # into their steady-state distribution from the first frame.
        head_start = random.uniform(0.0, 0.85)
        await asyncio.sleep(random.uniform(0.0, 0.4))
        while alive():
            # Snap (1 ms tween) back above the field with fresh glyphs
            # (or, on the first cycle, to the seeded mid-fall position).
            start_y = -1.05 + head_start * (travel + 1.05)
            drop.animate_offset = SNAP
            drop.offset = ft.Offset(0, start_y)
            for t in texts:
                t.value = random.choice(GLYPHS)
            page.update()
            await asyncio.sleep(0.15 if head_start else
                                random.uniform(0.3, 2.0))
            if not alive():
                return
            # One linear tween carries the rest of the fall at the same
            # speed a full-height fall would have; Flutter interpolates.
            dur = random.randint(*FALL_MS)
            drop.animate_offset = ft.Animation(int(dur * (1 - head_start)),
                                               ft.AnimationCurve.LINEAR)
            drop.offset = ft.Offset(0, travel)
            page.update()
            await asyncio.sleep(dur * (1 - head_start) / 1000)
            head_start = 0.0

    for drop, texts, travel in drops:
        page.run_task(run_drop, drop, texts, travel)

    return ft.Container(
        content=ft.Stack([d for d, _, _ in drops],
                         width=width, height=height),
        width=width,
        height=height,
        # No panel chrome: the glyphs rain straight on the page surface and
        # the clip bounds stay invisible.
        border_radius=20,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        # The rain reads as texture, not content; damp it as a whole.
        opacity=0.8 if theme.MODE == "dark" else 0.65,
    )


def rain_backdrop(page: ft.Page, *, width: int = 1920, height: int = 560,
                  columns: int = 48) -> ft.Control:
    """The site-wide backdrop: a full-width rain band under two masks.

    A vertical gradient dissolves the drops toward the bottom of the band so
    there is no hard clip line, and a horizontal mask knocks the glyphs down
    to a whisper (5%) over the content column's text zone: the hero intro
    has no card behind it, so glyphs there fight the name and tagline. The
    band and the 1080px content column are both centered, so the text zone
    lands at fixed fractions of the band width (left 58% of the column ~=
    22%..54% of 1920) at any viewport size.
    """
    band = ft.ShaderMask(
        content=matrix_rain(page, width=width, height=height,
                            columns=columns),
        blend_mode=ft.BlendMode.DST_IN,
        shader=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=[ft.Colors.WHITE, ft.Colors.TRANSPARENT],
        ),
    )
    clear = ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
    return ft.ShaderMask(
        content=band,
        blend_mode=ft.BlendMode.DST_IN,
        shader=ft.LinearGradient(
            begin=ft.Alignment.CENTER_LEFT,
            end=ft.Alignment.CENTER_RIGHT,
            colors=[ft.Colors.WHITE, ft.Colors.WHITE, clear, clear,
                    ft.Colors.WHITE, ft.Colors.WHITE],
            stops=[0.0, 0.13, 0.20, 0.56, 0.63, 1.0],
        ),
    )
