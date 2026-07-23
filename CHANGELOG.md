# Changelog

All notable changes to the portfolio site. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

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
  curated set of seven palettes: labforge's Paper, Neon Gold, Mint and
  Lavender, plus three custom palettes built from coolors.co seeds (Ember,
  Olive, Prism).
  `theme.py` holds the palette registry and an `apply(name)` that rebinds the
  colour constants; the router rebuilds the active view so the new palette
  (and light/dark mode) takes effect. The choice persists across reloads via
  `SharedPreferences` (a saved theme that no longer exists falls back to
  Paper).
- Teaching page (`/teaching`): profile, TA/tutoring roles, courses prepared
  to teach, mentoring & outreach; new "Teaching" navbar item.
- Slides PDFs for all talks (`src/assets/talks/`), linked with a
  "Slides (PDF)" button on each presentation card (HNL Seminar 2025 slides
  shared by the Brookhaven and Stony Brook seminars).
- Ph.D. thesis defense entry on the talks page and a "Defense slides (PDF)"
  button beside the eScholarship link on the hero thesis card.

### Changed

- Recropped the headshot to a face-centered square (from the high-res
  original) so the face sits in the middle of the circular frame.
- Removed the "Hi, I'm" greeting on the hero and the "+ labforge's paper
  theme" credit in the footer.
- Compressed the talk PDFs with Ghostscript (/ebook, ~64 MB → ~28 MB total).
- Removed em-dashes from all user-facing site text (tagline, CV bullets,
  teaching text, project descriptions, contact blurb, page title).
- Fixed stale labforge card text: the site uses the 'paper' design system,
  not 'instrument'.

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
