# Changelog

All notable changes to the portfolio site. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.5.1] - 2026-07-27

### Added

- The two 2021 biophysics papers now carry a figure each: the remdesivir
  versus ATP insertion comparison in the SARS-CoV-2 polymerase (MSDE) and the
  survey of viral polymerase folds and conserved motifs (CSBJ). Every
  publication on the page now has at least one figure.

### Changed

- A publication card holding a single figure keeps the same 135 px thumbnail
  height as the multi-figure strips, and its caption line reads "Select
  figure. Click to enlarge."
- `tools/build_media.py` can encode figures as JPEG: an output name ending in
  ".jpg" goes out as JPEG (quality 85) instead of PNG. The two new figures are
  rendered molecular structures rather than line-art plots, so PNG cost 1.6 MB
  and 490 KB where JPEG costs 500 KB and 160 KB.

## [0.5.0] - 2026-07-27

### Added

- The talks page is now Papers/Talks: a Publications section leads the page
  with each paper's abstract behind a "Show abstract" toggle and a strip of
  select figures (click to enlarge, caption in the lightbox). The two HNL
  papers carry four and two figures respectively, sized to fit the content
  column without scrolling; the earlier biophysics papers render as plain
  citations.
- Talk cards now show rendered slide previews (title slide plus two content
  slides per deck).
- A Talks & Presentations section on the CV page: a compact citation list of
  the same seven talks.
- The hero's thesis card shows two figures from the thesis (HNL branching
  fractions and the ATLAS/FASER2 signal topology) and the dissertation
  abstract behind the same "Show abstract" toggle, which now lives in
  `components/section.py` so both pages share it.
- The glyph rain now also runs behind the contact page, masked across the
  full content column (`rain_backdrop(..., text_zone=)`).
- `tools/build_media.py` renders both asset families: paper figures from the
  private `content/figures/` sources, and talk-slide previews from the
  committed deck PDFs. The slides rendered per deck live in its `TALK_SLIDES`
  map, and the figure strips wrap instead of scrolling, so a narrow viewport
  pushes the overflow onto a second line rather than hiding it.

### Changed

- Corrected the thesis title to "GeV-Scale Neutrinos: Modeling, Discovery and
  Characterization at Forward Physics Experiments". It comes from one
  constant, so the hero card, the CV education entry, and the defense listing
  all follow.
- Navbar label "Talks" is now "Papers/Talks"; the mobile collapse breakpoint
  moves from 780px to 850px to fit it.
- The contact page no longer links the Ph.D. thesis (it is still on the
  hero).
- Project cards no longer show screenshots: the `screenshots` lists are empty
  pending new captures. The card machinery is unchanged, so refilling a list
  restores the strip.

## [0.4.0] - 2026-07-27

### Added

- New site typography. Space Mono is the page-wide font (bundled, replacing
  the default sans), and the hero name + DLR brand mark render in Nabla, a
  COLRv1 color font instanced at extrusion depth 180 / edge highlight 12 and
  recolored to match every palette: light themes get a monochrome accent
  ramp, dark themes an accent face over a muted counterpoint extrusion
  (`tools/build_nabla_fonts.py` generates the 16 bundled builds, one base +
  one brighter "glint" per theme, subset to printable ASCII). Roboto Mono
  stays bundled for the glyph rain, which needs Greek coverage Space Mono
  lacks.
- The name shimmer works on the color font by sweeping a brighter build of
  the same font across the letters (color fonts ignore text colour), and the
  wave/glint timings are now explicit: the wave crosses the name in 1 s, the
  glint in 250 ms (`wave_text` in `src/components/wordmark.py`).

### Changed

- Default theme is now `neon_gold` (dark, pale gold accent on black with
  violet counterpoints) instead of `matrix`; unknown saved theme names fall
  back to it too (`src/theme.py`). All palettes stay in the picker, and the
  hero glyph rain follows whatever palette is active.

## [0.3.1] - 2026-07-23

### Fixed

- Mobile navbar overflow: on narrow viewports the horizontal link row plus
  theme picker overflowed and clipped ("Home CV Talks Teaching Proje..."),
  leaving the bar unusable. The navbar is now responsive
  (`src/components/navbar.py`): at/below 780px it collapses to a brand +
  hamburger row, and the hamburger toggles a stacked drop-down menu (the six
  links as full-width tap targets plus the theme picker below a divider).
  Wide viewports keep the original horizontal bar. The layout is chosen at
  build time from `page.width` and re-chosen live on `page.on_resize`.

## [0.3.0] - 2026-07-23

### Added

- Matrix-style physics-glyph rain behind the hero
  (`src/components/matrix_rain.py`): columns of Greek letters, operators and
  digits (RobotoMono-covered set) fall across a full-width band at the top of
  the home page, in theme accent colours with a secondary-colour minority.
  Flutter's implicit animations carry each fall, so the Pyodide runtime only
  retargets drops a few times per second; drops seed mid-flight so the field
  opens in its steady-state distribution, a vertical gradient dissolves the
  band toward the bottom, and a second mask knocks the glyphs down to 5%
  over the hero intro text (which has no card behind it).
- Matrix palette: phosphor green (#00FF41) on black with an amber terminal
  counterpoint as the secondary colour, designed to match the glyph rain.
- Motion pass inspired by labforge 0.3.0's UI polish:
  - Persistent navbar shell: navigation now swaps only the page body (with a
    soft fade) instead of rebuilding the whole view, and the active nav link
    gets an animated sliding underline.
  - Terminal brand mark: a terminal glyph on an accent tile next to "DLR"
    (labforge's app-mark style); the DLR letters scatter apart on hover and
    spring back (ported from labforge's animated wordmark).
  - Hero name animation: "Daniel La Rocco" plays a slow letter-by-letter wave
    followed by an accent-colour shimmer sweep, once on load and again on
    hover; the hero row fades in and rises on mount.
  - Hover motion: project screenshots (clickable, they open the lightbox)
    scale up slightly on hover.
  - Roboto Mono accents (bundled in `assets/fonts/`): brand, section kickers,
    tech chips, and timeline dates now use labforge's instrument-panel mono.
- Theme picker in the navbar: a dropdown that switches the site between a
  curated set of eight palettes: Matrix, labforge's Paper, Neon Gold, Mint
  and Lavender, plus three custom palettes built from coolors.co seeds
  (Ember, Olive, Prism).
  `theme.py` holds the palette registry and an `apply(name)` that rebinds the
  colour constants; the router rebuilds the active view so the new palette
  (and light/dark mode) takes effect. The choice persists across reloads via
  `SharedPreferences` (a saved theme that no longer exists falls back to the
  default).
- Teaching page (`/teaching`): profile, TA/tutoring roles, courses prepared
  to teach, mentoring & outreach; new "Teaching" navbar item.
- Slides PDFs for all talks (`src/assets/talks/`), linked with a
  "Slides (PDF)" button on each presentation card (HNL Seminar 2025 slides
  shared by the Brookhaven and Stony Brook seminars).
- Ph.D. thesis defense entry on the talks page and a "Defense slides (PDF)"
  button beside the eScholarship link on the hero thesis card.

### Changed

- Matrix is the default theme (was Paper); it leads the picker order and is
  the fallback for unknown saved theme names.
- The hero name shimmer sweeps more slowly (50 ms per letter, was 15 ms).
- Recropped the headshot to a face-centered square (from the high-res
  original) so the face sits in the middle of the circular frame.
- Removed the "Hi, I'm" greeting on the hero and the "+ labforge's paper
  theme" credit in the footer.
- Compressed the talk PDFs with Ghostscript (/ebook, ~64 MB → ~28 MB total).
- Removed em-dashes from all user-facing site text (tagline, CV bullets,
  teaching text, project descriptions, contact blurb, page title).
- Fixed stale labforge card text: the site uses the 'paper' design system,
  not 'instrument'.

### Fixed

- Thesis defense date on the talks page: May 2026 (was listed as Jun 2026).

## [0.2.0] - 2026-07-22

### Changed

- Switched the site color scheme from labforge's dark "instrument" theme to
  its light "paper" theme (warm paper surfaces, graphite ink, vermilion
  accent; steel-blue secondary, dark-rust highlight for text contrast).

### Added

- LinkedIn and ORCID links on the contact page.

## [0.1.0] - 2026-07-22

### Added

- Initial site: routed Flet SPA with hero, CV, presentations, projects, and
  contact views.
- Project registry (`src/data/projects.py`) featuring labforge and FORESEE
  Lab with screenshot galleries, plus HNLCalc and FORESEE research-software
  cards; conditional GitHub / PyPI / live-demo / docs buttons.
- Dark "instrument" theme adopted from labforge's design system.
- Ph.D. thesis feature card linking to eScholarship.
- GitHub Actions workflow building `flet build web` and deploying to GitHub
  Pages.
- Repo docs: CLAUDE.md (architecture + privacy rule), TASKLOG.md.
